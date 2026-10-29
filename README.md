# TPFI — Singleton Proxy Observer

Trabajo Práctico Final Integrador de **Ingeniería de Software II**
(UADER — Facultad de Ciencia y Tecnología).

Implementación en Python de tres patrones de diseño —**Singleton**, **Proxy**
y **Observer**— sobre comunicación por sockets TCP, con persistencia en
AWS DynamoDB.

## Descripción

El sistema está compuesto por tres programas:

| Programa | Rol | Patrón |
|---|---|---|
| `singletonproxyobserver` | Servidor proxy que atiende a los clientes | Proxy |
| `singletonclient` | Cliente que consulta y modifica datos | Singleton (acceso) |
| `observerclient` | Cliente que se suscribe y recibe notificaciones | Observer |

El servidor expone dos tablas de DynamoDB a través de un singleton:

- **`CorporateData`** — datos corporativos (`id`, `CUIT`, `razon_social`, etc.).
- **`CorporateLog`** — auditoría de cada operación (`uuid`, `sesion`, `accion`, `id`, `timestamp`).

## Acciones soportadas

| Acción | Requiere `ID` | Descripción |
|---|---|---|
| `get` | Sí | Devuelve el registro con ese `id`, o `Error` |
| `set` | No (va en `data`) | Crea o actualiza el registro y notifica a los suscriptos |
| `list` | No | Devuelve un array con todos los registros |
| `subscribe` | No | Registra el socket como suscriptor de cambios |

El `set` hace **merge parcial**: los campos no informados conservan su valor anterior, o quedan en blanco si el registro es nuevo.

## Estructura del proyecto

```text
TPFI/
├── src/tpfi/
│   ├── singletonproxyobserver.py   # servidor proxy
│   ├── singletonclient.py          # cliente get/set/list
│   ├── observerclient.py           # cliente suscriptor
│   └── soporte/
│       ├── database_singleton.py   # Singleton de acceso a DynamoDB
│       └── observer.py             # Subject / Observer
├── tests/
│   ├── test_aceptacion.py
│   └── test_patrones.py
├── docs/
├── CONTEXT.md
├── CHANGELOG.md
├── REQUIREMENTS.TXT
├── VERSION
├── BUILD
├── LICENSE
└── pyproject.toml
```

## Requisitos

- Python 3.12+
- Entorno virtual (`venv`)
- Credenciales de AWS con acceso a DynamoDB (región y nombres de tabla configurables)

## Instalación

```bash
python -m venv entorno_virtual
entorno_virtual\Scripts\activate
pip install -r REQUIREMENTS.TXT
```

## Uso

### Servidor

```bash
python -m src.tpfi.singletonproxyobserver -p=8080 -v
```

### Cliente

```bash
python -m src.tpfi.singletonclient -i=input.json -o=output.json -v
```

### Observer

```bash
python -m src.tpfi.observerclient -s=localhost -p=8080 -o=output.json -v
```

## Formato de los archivos JSON

### Entrada del cliente

```json
{
  "UUID": "123456789",
  "ID": "1",
  "ACTION": "get"
}
```

### Entrada del observer

```json
{
  "UUID": "123456789",
  "ACTION": "subscribe"
}
```

## Tests

```bash
pytest -v
pytest --cov=src --cov-report=term-missing
```

## Calidad de código

```bash
ruff check .
black --check .
mypy src/
pyright src/
bandit -r src/
```

## Documentación

```bash
pdoc src/tpfi -o docs/
```

## Versión y build

La versión vigente está en `VERSION` y el número de build en `BUILD`. El historial de cambios se mantiene en [CHANGELOG.md](CHANGELOG.md) y el registro de prompts de IA en [CONTEXT.md](CONTEXT.md).

## Licencia

MIT — ver [LICENSE](LICENSE).
