from scripts.tests.client import ApiClient
from scripts.tests.reporter import TestReporter

def run_route_tests(client: ApiClient, reporter: TestReporter, creator_id: int):
    module = "Rutas & POIs"
    print(f"\n--- Ejecutando Pruebas de {module} ---")

    # 1. Crear ruta con paradas
    route_payload = {
        "title": "Ruta de Prueba Automatizada",
        "start": "Plaza Principal",
        "destination": "Mirador de Tacna",
        "description": "Ruta generada para validación de endpoints",
        "distance_km": 4.5,
        "duration_min": 25,
        "fare": 3.0,
        "category_name": "Turística",
        "stops": ["Plaza Principal", "Parada Intermedia", "Mirador de Tacna"]
    }

    status, created_route, latency = client.post(
        "/api/v1/routes/",
        data=route_payload,
        params={"creator_id": creator_id}
    )
    has_dual_props = (
        isinstance(created_route, dict)
        and "distanceKm" in created_route
        and "creatorName" in created_route
        and len(created_route.get("stops", [])) == 3
    )
    success = status == 200 and has_dual_props
    reporter.log_result(
        module, "POST /api/v1/routes/", "POST", 200, status, latency, success,
        "(Dual props frontend OK)" if has_dual_props else "(Faltan props front)"
    )

    route_id = created_route.get("id") if isinstance(created_route, dict) else None

    # 2. Listar rutas generales
    status, list_res, latency = client.get("/api/v1/routes/")
    success = status == 200 and isinstance(list_res, list) and len(list_res) > 0
    reporter.log_result(module, "GET /api/v1/routes/", "GET", 200, status, latency, success)

    # 3. Filtrar por búsqueda de texto
    status, search_res, latency = client.get("/api/v1/routes/", params={"search": "Mirador"})
    success = status == 200 and any("Mirador" in r.get("destination", "") for r in search_res)
    reporter.log_result(module, "GET /api/v1/routes/?search=Mirador", "GET", 200, status, latency, success)

    # 4. Filtrar por categoría
    status, cat_res, latency = client.get("/api/v1/routes/", params={"category": "Turística"})
    success = status == 200 and all(r.get("category") == "Turística" for r in cat_res)
    reporter.log_result(module, "GET /api/v1/routes/?category=Turística", "GET", 200, status, latency, success)

    # 5. Filtrar por creador
    status, my_routes, latency = client.get("/api/v1/routes/", params={"creator_id": creator_id})
    success = status == 200 and all(r.get("creator_id") == creator_id for r in my_routes)
    reporter.log_result(module, f"GET /api/v1/routes/?creator_id={creator_id}", "GET", 200, status, latency, success)

    if route_id:
        # 6. Obtener detalle de ruta por ID
        status, detail_res, latency = client.get(f"/api/v1/routes/{route_id}")
        success = status == 200 and detail_res.get("id") == route_id and len(detail_res.get("points", [])) == 3
        reporter.log_result(module, f"GET /api/v1/routes/{route_id}", "GET", 200, status, latency, success)

        # 7. Actualizar ruta
        up_payload = {"title": "Ruta de Prueba - Título Actualizado", "fare": 3.5}
        status, up_res, latency = client.put(f"/api/v1/routes/{route_id}", data=up_payload, params={"user_id": creator_id})
        success = status == 200 and up_res.get("title") == up_payload["title"]
        reporter.log_result(module, f"PUT /api/v1/routes/{route_id}", "PUT", 200, status, latency, success)

    return route_id
