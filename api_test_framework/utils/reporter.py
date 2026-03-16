"""
JSON Report Generator
Produces a machine-readable JSON summary of each test run.
"""

import json
import time
from datetime import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


class JSONReporter:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    def record(self, test_name: str, status: str, duration_ms: float,
               endpoint: str = "", method: str = "", status_code: int = None,
               error: str = ""):
        self.results.append({
            "test": test_name,
            "status": status,          # PASS | FAIL | ERROR | SKIP
            "duration_ms": round(duration_ms, 2),
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def save(self, filename: str = None) -> Path:
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")

        summary = {
            "run_at": datetime.utcnow().isoformat(),
            "duration_s": round(time.time() - self.start_time, 2),
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": f"{(passed / total * 100):.1f}%" if total else "N/A",
            "results": self.results,
        }

        filename = filename or f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        path = REPORTS_DIR / filename
        with open(path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n📄 JSON report saved → {path}")
        return path
