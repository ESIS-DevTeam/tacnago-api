from scripts.tests.client import ApiClient
from scripts.tests.reporter import TestReporter

def run_category_tests(client: ApiClient, reporter: TestReporter):
    module = "Categorías"
    print(f"\n--- Ejecutando Pruebas de {module} ---")

    # 1. Listar categorías
    status, data, latency = client.get("/api/v1/categories/")
    success = status == 200 and isinstance(data, list)
    reporter.log_result(module, "GET /api/v1/categories/", "GET", 200, status, latency, success)

    # 2. Crear categoría
    new_cat = {"name": "Test Cat Temporal", "description": "Para prueba automatizada"}
    status, cat_created, latency = client.post("/api/v1/categories/", data=new_cat)
    success = status == 200 and cat_created.get("name") == new_cat["name"]
    reporter.log_result(module, "POST /api/v1/categories/", "POST", 200, status, latency, success)

    cat_id = cat_created.get("id") if isinstance(cat_created, dict) else None

    if cat_id:
        # 3. Obtener por ID
        status, cat_fetched, latency = client.get(f"/api/v1/categories/{cat_id}")
        success = status == 200 and cat_fetched.get("id") == cat_id
        reporter.log_result(module, f"GET /api/v1/categories/{cat_id}", "GET", 200, status, latency, success)

        # 4. Actualizar categoría
        update_payload = {"name": "Test Cat Modificada", "description": "Modificado"}
        status, cat_updated, latency = client.put(f"/api/v1/categories/{cat_id}", data=update_payload)
        success = status == 200 and cat_updated.get("name") == "Test Cat Modificada"
        reporter.log_result(module, f"PUT /api/v1/categories/{cat_id}", "PUT", 200, status, latency, success)

        # 5. Eliminar categoría
        status, del_res, latency = client.delete(f"/api/v1/categories/{cat_id}")
        success = status == 200
        reporter.log_result(module, f"DELETE /api/v1/categories/{cat_id}", "DELETE", 200, status, latency, success)

        # 6. Verificar 404 al consultar eliminada
        status, _, latency = client.get(f"/api/v1/categories/{cat_id}")
        success = status == 404
        reporter.log_result(module, f"GET /api/v1/categories/{cat_id} (eliminada)", "GET", 404, status, latency, success)
