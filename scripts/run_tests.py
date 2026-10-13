import argparse
import sys
from scripts.tests.client import ApiClient
from scripts.tests.reporter import TestReporter
from scripts.tests.test_categories import run_category_tests
from scripts.tests.test_users import run_user_tests
from scripts.tests.test_routes import run_route_tests
from scripts.tests.test_social import run_social_tests

def main():
    parser = argparse.ArgumentParser(description="Suite de Pruebas Automatizadas de TacnaGo API")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="URL base de la API (por defecto: http://127.0.0.1:8000)"
    )
    parser.add_argument(
        "--module",
        choices=["all", "categories", "users", "routes", "social"],
        default="all",
        help="Módulo específico a probar o 'all' para todo el backend"
    )
    args = parser.parse_args()

    client = ApiClient(base_url=args.url)
    reporter = TestReporter()

    print("=" * 70)
    print("      INICIANDO SUITE DE PRUEBAS AUTOMATIZADAS - TACNAGO API")
    print(f"      Destino: {args.url} | Módulo: {args.module.upper()}")
    print("=" * 70)

    # 1. Comprobar salud / conectividad del servidor
    status, res, latency = client.get("/")
    if status != 200:
        print("\n❌ ERROR: No se pudo conectar con la API en " + args.url)
        print("   Asegúrate de tener el servidor corriendo con:")
        print("   uvicorn main:app --reload\n")
        sys.exit(1)

    print(f"✅ Conexión con la API establecida con éxito ({latency:.2f} ms)\n")

    # Variables de contexto compartidas entre módulos
    test_user_id = None
    test_route_id = None

    # Ejecutar según módulo
    if args.module in ["all", "categories"]:
        run_category_tests(client, reporter)

    if args.module in ["all", "users", "routes", "social"]:
        test_user_id = run_user_tests(client, reporter)

    if args.module in ["all", "routes", "social"]:
        if not test_user_id:
            # Fallback a usuario demo si se ejecutó solo rutas
            _, login_res, _ = client.post("/api/v1/users/login", data={"email": "demo@tacnago.pe", "password": "123456"})
            test_user_id = login_res.get("id") if isinstance(login_res, dict) else 1
        test_route_id = run_route_tests(client, reporter, creator_id=test_user_id)

    if args.module in ["all", "social"]:
        if test_user_id and test_route_id:
            run_social_tests(client, reporter, user_id=test_user_id, route_id=test_route_id)

    # Imprimir resumen de métricas
    reporter.print_summary()

if __name__ == "__main__":
    main()
