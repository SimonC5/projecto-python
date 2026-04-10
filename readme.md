# gestion-info

Sistema de gestión de registros de personas desde consola, con persistencia en JSON y generación de datos falsos con Faker.

## Estructura del proyecto

```
gestion-info/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── records.json          # Base de datos local (JSON)
└── src/
    ├── main.py               # Demostración/prueba directa (sin menú)
    ├── menu.py               # Interfaz de consola — punto de entrada principal
    ├── service.py            # Lógica de negocio (CRUD)
    ├── file.py               # Persistencia (leer/guardar JSON)
    ├── validate.py           # Validaciones de campos
    └── integration.py        # Generación de datos falsos con Faker
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

La única dependencia externa es **Faker**, usada para generar registros de prueba.

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

### Opción 3 — Generar registros falsos

Al elegir la opción **3**, el sistema usa la librería `Faker` para crear 10 personas con datos aleatorios (nombre, email, edad, estado civil) y los guarda automáticamente en `data/records.json`.

### Ejecutar demostración directa

```bash
cd src
python main.py
```

Corre una secuencia de prueba con creaciones válidas e inválidas, sin interacción.

## Campos de un registro

| Campo    | Tipo   | Restricciones                                      |
|----------|--------|----------------------------------------------------|
| `id`     | string | No vacío, único                                    |
| `name`   | string | Solo letras y espacios                             |
| `email`  | string | Formato válido, único                              |
| `age`    | int    | Entre 0 y 120                                      |
| `status` | string | `single`, `married`, `widowed` o `divorced`        |

## Integración con Faker (`integration.py`)

El módulo `integration.py` expone dos funciones:

- **`build_record(*args, **kwargs)`** — función genérica que construye un dict de registro a partir de `**kwargs`. El uso de `*args` permite extensibilidad futura sin romper la firma.
- **`generate_fake_records(n=10)`** — genera `n` registros con datos aleatorios usando `Faker`.

