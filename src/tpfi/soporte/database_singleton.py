from decimal import Decimal

import boto3
from botocore.config import Config


def _convert(item):
    """Convierte Decimal de DynamoDB a int/float para poder serializar con json."""
    if isinstance(item, list):
        return [_convert(i) for i in item]
    if isinstance(item, dict):
        return {k: _convert(v) for k, v in item.items()}
    if isinstance(item, Decimal):
        return int(item) if item % 1 == 0 else float(item)
    return item


CAMPOS_CORPORATE_DATA = [
    "id", "cp", "CUIT", "domicilio", "idreq", "idSeq",
    "localidad", "provincia", "sede", "seqID", "telefono", "web",
]

# Cliente compartido con reintentos adaptativos: evita
# ProvisionedThroughputExceededException en tablas con capacidad baja.
_CLIENTE_DYNAMODB = boto3.resource(
    "dynamodb",
    config=Config(retries={"max_attempts": 20, "mode": "adaptive"}),
)


class CorporateDataDB:
    """Singleton-Acceso a tabla CorporateData"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._table = _CLIENTE_DYNAMODB.Table("CorporateData")
        return cls._instance

    def get(self, id):
        response = self._table.get_item(Key={"id": id})
        return _convert(response.get("Item"))

    def set(self, item):
        """Merge parcial: completa campos faltantes con el valor viejo o en blanco."""
        id = item.get("id")
        if id is None:
            raise ValueError("El registro debe incluir 'id'")

        # Lee el registro existente
        existente = self.get(id) or {}

        # Arma el registro final: prioridad al nuevo item, resto del existente o en blanco
        registro = {}
        for campo in CAMPOS_CORPORATE_DATA:
            if campo in item:
                registro[campo] = item[campo]
            elif campo in existente:
                registro[campo] = existente[campo]
            else:
                registro[campo] = ""

        self._table.put_item(Item=registro)
        return dict(item)

    def list(self):
        items = self._table.scan().get("Items", [])
        return _convert(items)


class CorporateLogDB:
    """Singleton- acceso a tabla CorporateLog"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._table = _CLIENTE_DYNAMODB.Table("CorporateLog")
        return cls.__instance

    def log(self, uuid, sesion, accion, id, timestamp):
        item = {
            "uuid": str(uuid),
            "sesion": str(sesion),
            "accion": accion,
            "id": id,
            "timestamp": str(timestamp),
        }
        self._table.put_item(Item=item)
        return item
