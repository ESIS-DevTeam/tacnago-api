from db.base import engine, SessionLocal, Base
from db.models.category import Category
from db.models.user import User
from db.models.route import Route
from db.models.route_point import RoutePoint
import db.models

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # 1. Sembrar categorías iniciales
        default_categories = [
            ("Transporte", "Rutas de movilidad urbana y transporte público"),
            ("Turística", "Circuitos turísticos y patrimonio cultural de Tacna"),
            ("Gastronómica", "Recorridos por zonas gastronómicas y restaurantes"),
            ("Comercial", "Circuitos de compras, mercadillos y centros comerciales"),
            ("Deportiva", "Rutas para running, ciclismo y deportes al aire libre"),
            ("General", "Rutas generales"),
        ]
        for name, desc in default_categories:
            if not db.query(Category).filter_by(name=name).first():
                db.add(Category(name=name, description=desc))
        db.commit()

        # 2. Sembrar usuario de prueba
        if not db.query(User).filter_by(email="demo@tacnago.pe").first():
            demo_user = User(
                name="Aramis Claros",
                email="demo@tacnago.pe",
                password="123456",
                avatar="",
                bio="Descubriendo Tacna, una ruta a la vez."
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

            # Sembrar ruta de ejemplo
            cat = db.query(Category).filter_by(name="Comercial").first()
            route = Route(
                title="Ruta 1 - Centro",
                start="Mercado Central",
                destination="Paseo Cívico",
                description="Del Mercado Central al Paseo Cívico, por Av. Bolognesi.",
                fare=2.0,
                distance_km=2.4,
                duration_min=12,
                rating=5.0,
                category_id=cat.id if cat else 1,
                creator_id=demo_user.id
            )
            db.add(route)
            db.commit()
            db.refresh(route)

            stops = ["Mercado Central", "Av. Bolognesi", "Paseo Cívico"]
            for idx, stop in enumerate(stops):
                db.add(RoutePoint(
                    route_id=route.id,
                    name=stop,
                    latitude=0.0,
                    longitude=0.0,
                    order=idx
                ))
            db.commit()

        print("✅ Datos semilla cargados con éxito")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
