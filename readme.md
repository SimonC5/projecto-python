# gestion-info

Sistema de gestión de registros de personas desde consola, con persistencia en JSON y generación de datos falsos con Faker.

## Estructura del proyecto

```
gestion-info/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── records.json              # Base de datos local (JSON)
├── src/
│   ├── main.py                   # Demo/smoke-test sin menú interactivo
│   ├── menu.py                   # Interfaz de consola — punto de entrada principal
│   ├── service.py                # Lógica de negocio (CRUD + unicidad)
│   ├── storage.py                # Persistencia (leer/guardar JSON)
│   ├── validate.py               # Validaciones de campos (sin efectos secundarios)
│   └── integration.py            # Generación de datos falsos con Faker
└── tests/
    ├── conftest.py               # Fixtures compartidos (storage temporal)
    ├── test_validate.py          # Tests unitarios de cada validador
    ├── test_service.py           # Tests de RegisterService (CRUD, unicidad, persistencia)
    └── test_integration.py       # Tests del generador de datos falsos
```

## Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repo>
cd gestion-info
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación con menú interactivo

```bash
cd src
python menu.py
```

Verás el menú principal:

```
────────────────────────────────────────────────────────
  GESTIÓN DE REGISTROS — MENÚ PRINCIPAL
────────────────────────────────────────────────────────
  1. Crear registro
  2. Listar registros
  3. Generar 10 registros falsos (Faker)
  0. Salir
```

### Ejecutar la demo sin interacción

```bash
cd src
python main.py
```

## Ejecutar las pruebas

Desde la raíz del proyecto:

```bash
pytest tests/ -v
```

Para ver un resumen corto (sin detalle de cada test):

```bash
pytest tests/
```

Para ejecutar solo un módulo de tests:

```bash
pytest tests/test_validate.py -v
pytest tests/test_service.py  -v
```

### Cobertura (opcional)

```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=term-missing
```

## Campos de un registro

| Campo    | Tipo   | Restricciones                                      |
|----------|--------|----------------------------------------------------|
| `id`     | string | No vacío, único                                    |
| `name`   | string | Solo letras y espacios (admite tildes y ñ)         |
| `email`  | string | Formato válido, único (comparación case-insensitive)|
| `age`    | int    | Entre 0 y 120                                      |
| `status` | string | `single`, `married`, `widowed` o `divorced`        |

## Arquitectura y decisiones de diseño

### Separación de responsabilidades

| Módulo          | Responsabilidad única                                        |
|-----------------|--------------------------------------------------------------|
| `validate.py`   | Validar un campo en aislamiento; sin efectos secundarios     |
| `storage.py`    | Leer y escribir el archivo JSON; sin lógica de negocio       |
| `service.py`    | Orquestar validaciones, unicidad y persistencia              |
| `menu.py`       | Recoger entrada del usuario y delegar a `service`            |
| `integration.py`| Generar datos de prueba con Faker                            |

### Cambios respecto a la versión anterior

- `file.py` renombrado a `storage.py` para reflejar su responsabilidad real.
- Los sets `REGISTERED_IDS` y `REGISTERED_EMAILS` se movieron de `validate.py` a `RegisterService`, que es quien conoce el estado global.
- `validate_*` solo validan formato; la unicidad la comprueba el servicio antes de llamarlos.
- `menu.py` no contiene ninguna lógica de negocio ni validación propia.
- Type hints y docstrings en todos los módulos públicos.

## Integración con Faker (`integration.py`)

- **`build_record(**kwargs)`** — construye un dict de registro a partir de keyword arguments. Valores por defecto seguros para campos no proporcionados.
- **`generate_fake_records(n=10)`** — genera `n` registros aleatorios con unicidad de email garantizada dentro del lote.