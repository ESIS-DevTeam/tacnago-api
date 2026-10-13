import time
from scripts.tests.client import ApiClient
from scripts.tests.reporter import TestReporter

def run_user_tests(client: ApiClient, reporter: TestReporter):
    module = "Usuarios"
    print(f"\n--- Ejecutando Pruebas de {module} ---")

    test_email = f"tester_{int(time.time())}@tacnago.pe"
    test_password = "password123"

    # 1. Registrar usuario
    user_payload = {
        "name": "Usuario Test Automatizado",
        "email": test_email,
        "password": test_password,
        "bio": "Cuenta de prueba automática"
    }
    status, reg_res, latency = client.post("/api/v1/users/register", data=user_payload)
    no_password_exposed = "password" not in reg_res if isinstance(reg_res, dict) else False
    success = status == 200 and reg_res.get("email") == test_email and no_password_exposed
    reporter.log_result(
        module, "POST /api/v1/users/register", "POST", 200, status, latency, success,
        "(Contraseña protegida)" if no_password_exposed else "(ALERTA: Password expuesto)"
    )

    user_id = reg_res.get("id") if isinstance(reg_res, dict) else None

    # 2. Registrar duplicado (debe dar 400)
    status, dup_res, latency = client.post("/api/v1/users/register", data=user_payload)
    success = status == 400
    reporter.log_result(module, "POST /api/v1/users/register (duplicado)", "POST", 400, status, latency, success)

    # 3. Login con contraseña correcta (200)
    login_payload = {"email": test_email, "password": test_password}
    status, login_res, latency = client.post("/api/v1/users/login", data=login_payload)
    success = status == 200 and login_res.get("id") == user_id
    reporter.log_result(module, "POST /api/v1/users/login (exitoso)", "POST", 200, status, latency, success)

    # 4. Login con contraseña errónea (debe dar 401)
    bad_login_payload = {"email": test_email, "password": "wrongpassword"}
    status, _, latency = client.post("/api/v1/users/login", data=bad_login_payload)
    success = status == 401
    reporter.log_result(module, "POST /api/v1/users/login (clave inválida)", "POST", 401, status, latency, success)

    # 5. Obtener usuario por ID
    if user_id:
        status, get_res, latency = client.get(f"/api/v1/users/{user_id}")
        success = status == 200 and get_res.get("id") == user_id
        reporter.log_result(module, f"GET /api/v1/users/{user_id}", "GET", 200, status, latency, success)

        # 6. Actualizar perfil
        update_data = {"bio": "Biografía actualizada por script de test"}
        status, up_res, latency = client.put(f"/api/v1/users/{user_id}", data=update_data)
        success = status == 200 and up_res.get("bio") == update_data["bio"]
        reporter.log_result(module, f"PUT /api/v1/users/{user_id}", "PUT", 200, status, latency, success)

    return user_id
