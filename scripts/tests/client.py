import json
import time
import urllib.request
import urllib.error
from typing import Any, Optional, Dict, Tuple

class ApiClient:
    """Cliente HTTP ligero basado en urllib para no requerir dependencias externas."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, Any, float]:
        """
        Ejecuta una petición HTTP y mide el tiempo de respuesta.
        Retorna (status_code, json_response_o_texto, latency_ms).
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            url = f"{url}?{query_string}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = json.dumps(data).encode("utf-8") if data is not None else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)

        start_time = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                latency_ms = (time.perf_counter() - start_time) * 1000
                res_body = response.read().decode("utf-8")
                try:
                    parsed_data = json.loads(res_body)
                except Exception:
                    parsed_data = res_body
                return response.status, parsed_data, latency_ms
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            err_body = e.read().decode("utf-8")
            try:
                parsed_data = json.loads(err_body)
            except Exception:
                parsed_data = err_body
            return e.code, parsed_data, latency_ms
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            return 0, {"error": str(e)}, latency_ms

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None):
        return self.request("POST", endpoint, data=data, params=params)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None):
        return self.request("PUT", endpoint, data=data, params=params)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None):
        return self.request("PATCH", endpoint, data=data, params=params)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        return self.request("DELETE", endpoint, params=params)
