from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.routes import user_routes, category_routes, route_routes, social_routes

app = FastAPI(title="TacnaGo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(category_routes.router, prefix="/api/v1/categories", tags=["Categorías"])
app.include_router(route_routes.router, prefix="/api/v1/routes", tags=["Rutas"])
app.include_router(social_routes.router, prefix="/api/v1", tags=["Social y Comunidad"])

@app.get("/")
def read_root():
    return {"message": "TacnaGo API funcionando correctamente"}