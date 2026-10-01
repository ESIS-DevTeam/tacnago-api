# TacnaGo API

Backend de **TacnaGo**, una aplicación web para rutas turísticas y puntos de interés de la ciudad de Tacna.

## Tecnologías

- Python 3.10+
- FastAPI y Uvicorn
- SQLAlchemy
- Pydantic v2 y pydantic-settings
- PostgreSQL mediante Supabase

## Requisitos

- Python 3.10 o superior.
- Un proyecto de Supabase con una base de datos PostgreSQL.

## Instalación local

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone https://github.com/ESIS-DevTeam/tacnago-api.git
cd tacnago
```

Crea y activa un entorno virtual:

```bash
python -m venv venv

# Windows PowerShell
venv/Scripts/activate

# Linux/macOS
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Configura la conexión de Supabase en un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL="<url>"
```

Usa la cadena de conexión PostgreSQL proporcionada por Supabase.

Después de configurar la conexión, crea las tablas ejecutando una vez:

```bash
python database.py
```

Inicia el servidor:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Documentación de la API

Con el servidor iniciado:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Esquema OpenAPI: `http://127.0.0.1:8000/openapi.json`
- Comprobación básica: `GET /`

## Estructura del proyecto

```text
tacnago-api/
├── api/v1/routes/       # Endpoints FastAPI por recurso
├── core/                # Configuración de la aplicación
├── db/                  # Base SQLAlchemy y modelos
├── repositories/        # Acceso a datos
├── schemas/             # Validación y serialización Pydantic
├── services/            # Lógica de negocio
├── utils/               # Utilidades compartidas
├── database.py          # Inicialización de tablas en Supabase
├── main.py              # Aplicación FastAPI
├── requirements.txt     # Dependencias
└── .env                 # Configuración local
```