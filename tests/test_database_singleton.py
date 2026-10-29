"""Prueba patrón singleton y operaciones de base"""
from decimal import Decimal

from src.tpfi.soporte.database_singleton import CorporateDataDB, CorporateLogDB


def test_singleton_data():
    a = CorporateDataDB()
    b = CorporateDataDB()
    assert a is b


def test_singleton_log():
    a = CorporateLogDB()
    b = CorporateLogDB()
    assert a is b


def test_list_devuelve_lista():
    db = CorporateDataDB()
    resultado = db.list()
    assert isinstance(resultado, list)


def test_set_y_get_redondos():
    db = CorporateDataDB()
    item = {"id": "test-001", "valor": 42}
    db.set(item)
    obtenido = db.get("test-001")
    assert obtenido is not None
    assert obtenido.get("id") == "test-001"


def test_list_no_tiene_decimales():
    """DynamoDB devuelve Decimal; deben convertirse a int/float."""
    db = CorporateDataDB()
    for item in db.list():
        for valor in item.values():
            assert not isinstance(valor, Decimal)
