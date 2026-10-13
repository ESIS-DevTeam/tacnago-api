import time
from scripts.tests.client import ApiClient
from scripts.tests.reporter import TestReporter

def run_social_tests(client: ApiClient, reporter: TestReporter, user_id: int, route_id: int):
    module = "Social & Comunidad"
    print(f"\n--- Ejecutando Pruebas de {module} ---")

    # --- 1. Reseñas (Reviews) ---
    review_payload = {
        "rating": 5,
        "comment": "Excelente recorrido, muy bien detallado.",
        "route_id": route_id
    }
    status, rev_res, latency = client.post(
        f"/api/v1/routes/{route_id}/reviews",
        data=review_payload,
        params={"user_id": user_id}
    )
    success = status == 200 and rev_res.get("rating") == 5
    reporter.log_result(module, f"POST /api/v1/routes/{route_id}/reviews", "POST", 200, status, latency, success)

    status, rev_list, latency = client.get(f"/api/v1/routes/{route_id}/reviews")
    success = status == 200 and isinstance(rev_list, list) and len(rev_list) > 0
    reporter.log_result(module, f"GET /api/v1/routes/{route_id}/reviews", "GET", 200, status, latency, success)

    # Validar recálculo del rating en la ruta
    status, route_checked, latency = client.get(f"/api/v1/routes/{route_id}")
    rating_updated = route_checked.get("rating") == 5.0
    reporter.log_result(
        module, f"Validar Recálculo de Rating en Ruta", "CHECK", 200, status, latency, rating_updated,
        f"(Rating recalculado a {route_checked.get('rating')})"
    )

    # --- 2. Historial de Viajes (Recorridas) ---
    trip_payload = {"route_id": route_id, "fare": 3.5}
    status, trip_res, latency = client.post(
        "/api/v1/travel-history",
        data=trip_payload,
        params={"user_id": user_id}
    )
    success = status == 200 and trip_res.get("user_id") == user_id
    reporter.log_result(module, "POST /api/v1/travel-history", "POST", 200, status, latency, success)

    status, trips_list, latency = client.get("/api/v1/travel-history", params={"user_id": user_id})
    success = status == 200 and isinstance(trips_list, list) and len(trips_list) > 0
    reporter.log_result(module, f"GET /api/v1/travel-history?user_id={user_id}", "GET", 200, status, latency, success)

    # --- 3. Seguidores (Comunidad) ---
    # Creamos un segundo usuario para probar follow
    second_email = f"friend_{int(time.time())}@tacnago.pe"
    _, friend, _ = client.post("/api/v1/users/register", data={"name": "Amigo Test", "email": second_email, "password": "123"})
    friend_id = friend.get("id") if isinstance(friend, dict) else None

    if friend_id:
        # Seguir amigo
        status, follow_res, latency = client.post(
            "/api/v1/users/follow",
            data={"followed_id": friend_id},
            params={"follower_id": user_id}
        )
        success = status == 200 and follow_res.get("success") is True
        reporter.log_result(module, "POST /api/v1/users/follow", "POST", 200, status, latency, success)

        # Intentar auto-seguimiento (debe fallar 400)
        status, _, latency = client.post(
            "/api/v1/users/follow",
            data={"followed_id": user_id},
            params={"follower_id": user_id}
        )
        success = status == 400
        reporter.log_result(module, "POST /api/v1/users/follow (auto-follow)", "POST", 400, status, latency, success)

        # Dejar de seguir
        status, unfollow_res, latency = client.delete(
            f"/api/v1/users/unfollow/{friend_id}",
            params={"follower_id": user_id}
        )
        success = status == 200 and unfollow_res.get("success") is True
        reporter.log_result(module, f"DELETE /api/v1/users/unfollow/{friend_id}", "DELETE", 200, status, latency, success)

    # --- 4. Notificaciones ---
    status, notifs, latency = client.get("/api/v1/notifications", params={"user_id": user_id})
    success = status == 200 and isinstance(notifs, list)
    reporter.log_result(module, f"GET /api/v1/notifications?user_id={user_id}", "GET", 200, status, latency, success)

    # --- 5. Limpieza final de la ruta creada ---
    status, del_r, latency = client.delete(f"/api/v1/routes/{route_id}", params={"user_id": user_id})
    success = status == 200 and del_r.get("success") is True
    reporter.log_result(module, f"DELETE /api/v1/routes/{route_id} (limpieza)", "DELETE", 200, status, latency, success)
