from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TestResult:
    module: str
    endpoint: str
    method: str
    status_expected: int
    status_actual: int
    latency_ms: float
    success: bool
    message: str = ""

class TestReporter:
    def __init__(self):
        self.results: List[TestResult] = []

    def log_result(
        self,
        module: str,
        endpoint: str,
        method: str,
        status_expected: int,
        status_actual: int,
        latency_ms: float,
        success: bool,
        message: str = ""
    ):
        result = TestResult(
            module=module,
            endpoint=endpoint,
            method=method,
            status_expected=status_expected,
            status_actual=status_actual,
            latency_ms=latency_ms,
            success=success,
            message=message
        )
        self.results.append(result)
        icon = "✅" if success else "❌"
        status_str = f"[{result.status_actual}]"
        print(f"  {icon} {result.method:<6} {result.endpoint:<35} {status_str:<6} {result.latency_ms:>6.2f} ms {result.message}")

    def print_summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0
        latencies = [r.latency_ms for r in self.results if r.status_actual != 0]
        avg_latency = (sum(latencies) / len(latencies)) if latencies else 0
        min_latency = min(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0

        print("\n" + "=" * 70)
        print("                  REPORTE DE MÉTRICAS DE LA API")
        print("=" * 70)
        print(f"Total de Pruebas Ejecutadas : {total}")
        print(f"Pruebas Exitosas            : {passed} ✅")
        print(f"Pruebas Fallidas            : {failed} ❌")
        print(f"Tasa de Éxito (Success Rate): {success_rate:.1f}%")
        print("-" * 70)
        print(f"Latencia Promedio           : {avg_latency:.2f} ms")
        print(f"Latencia Mínima             : {min_latency:.2f} ms")
        print(f"Latencia Máxima             : {max_latency:.2f} ms")
        print("=" * 70)

        # Resumen por módulo
        modules = sorted(list(set(r.module for r in self.results)))
        print("\nDetalle por Módulo:")
        for mod in modules:
            mod_results = [r for r in self.results if r.module == mod]
            mod_passed = sum(1 for r in mod_results if r.success)
            mod_total = len(mod_results)
            mod_avg = sum(r.latency_ms for r in mod_results) / mod_total
            print(f" • {mod:<20}: {mod_passed}/{mod_total} exitosos | Latencia media: {mod_avg:.2f} ms")
        print()
