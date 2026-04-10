from tester.client import APIClient
from tester.tests import (
    test_status_code_200,
    test_content_type_json,
    test_required_fields,
    test_field_types,
    test_base_currency_eur,
    test_rates_not_empty,
    test_usd_rate_positive,
    test_date_format,
)


def run_all_tests():
    client = APIClient()
    response = client.get("/latest", params={"from": "EUR"})

    tests = [
        test_status_code_200(response),
        test_content_type_json(response),
        test_required_fields(response),
        test_field_types(response),
        test_base_currency_eur(response),
        test_rates_not_empty(response),
        test_usd_rate_positive(response),
        test_date_format(response),
    ]

    passed = sum(1 for t in tests if t["status"] == "PASS")
    failed = sum(1 for t in tests if t["status"] == "FAIL")
    latencies = [t["latency_ms"] for t in tests]

    summary = {
        "passed": passed,
        "failed": failed,
        "error_rate": round(failed / len(tests), 3) if tests else 0,
        "latency_ms_avg": round(sum(latencies) / len(latencies), 2) if latencies else 0,
        "latency_ms_p95": max(latencies) if latencies else 0,
    }

    return {
        "api": "Frankfurter",
        "summary": summary,
        "tests": tests,
    }
import traceback

@app.get("/run")
def run():
    try:
        result = run_all_tests()
        save_run(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }), 500
