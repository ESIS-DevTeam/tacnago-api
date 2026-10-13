# TacnaGo API

Backend de **TacnaGo**, una aplicación web y móvil para descubrir, trazar y compartir circuitos geolocalizados y rutas turísticas en la ciudad de Tacna, Perú.

## Tecnologías

- Python 3.10+
- FastAPI y Uvicorn
- SQLAlchemy
- Pydantic v2 y pydantic-settings
- PostgreSQL mediante Supabase

## Requisitos

- Python 3.10 o superior
- Un proyecto de Supabase con base de datos PostgreSQL

## Instalación local

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone https://github.com/ESIS-DevTeam/tacnago-api.git
cd tacnago-api
```

Crea y activa un entorno virtual:

```bash
python -m venv venv

# Windows PowerShell
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Configura la conexión de la base de datos en un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Crea las tablas en la base de datos:

```bash
python database.py
```

Puebla la base de datos con los datos iniciales (categorías y usuario demo):

```bash
python -m scripts.seed
```

Inicia el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

## Documentación de la API

Con el servidor iniciado:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Estructura del proyecto

```text
tacnago-api/
├── api/v1/routes/       # Endpoints FastAPI por recurso
├── core/                # Configuración de la aplicación
├── db/                  # Modelos y base SQLAlchemy
├── repositories/        # Acceso a datos
├── schemas/             # Validación y serialización Pydantic
├── scripts/             # Scripts de utilidad
│   ├── seed.py          # Carga de datos semilla iniciales
│   ├── run_tests.py     # Ejecutor de pruebas automatizadas y métricas
│   └── tests/           # Módulos de prueba por entidad
├── services/            # Lógica de negocio
├── utils/               # Utilidades compartidas (paginación)
├── database.py          # Inicialización de tablas
├── main.py              # Aplicación FastAPI
└── requirements.txt     # Dependencias del proyecto
```

## Pruebas automatizadas

El proyecto incluye una suite de pruebas automatizadas que valida todos los endpoints y genera un reporte de métricas de latencia y tasa de éxito:

```bash
# Probar todos los módulos
python -m scripts.run_tests

# Probar un módulo específico
python -m scripts.run_tests --module routes
python -m scripts.run_tests --module users
python -m scripts.run_tests --module categories
python -m scripts.run_tests --module social
```

## Licencia

Distribuido bajo la licencia MIT.