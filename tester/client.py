import time
import requests


class APIClient:
    def __init__(self, base_url="https://api.frankfurter.app", timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        start = time.perf_counter()

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "json": response.json() if "application/json" in response.headers.get("Content-Type", "") else None,
                "latency_ms": latency_ms,
                "error": None,
            }
        except requests.exceptions.RequestException as e:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return {
                "success": False,
                "status_code": None,
                "headers": {},
                "json": None,
                "latency_ms": latency_ms,
                "error": str(e),
            }
