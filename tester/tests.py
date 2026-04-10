import re


def test_status_code_200(response):
    passed = response["status_code"] == 200
    return {
        "name": "HTTP status = 200",
        "status": "PASS" if passed else "FAIL",
        "details": f"status_code={response['status_code']}",
        "latency_ms": response["latency_ms"],
    }


def test_content_type_json(response):
    content_type = response["headers"].get("Content-Type", "")
    passed = "application/json" in content_type
    return {
        "name": "Content-Type is JSON",
        "status": "PASS" if passed else "FAIL",
        "details": content_type,
        "latency_ms": response["latency_ms"],
    }


def test_required_fields(response):
    data = response["json"] or {}
    required = ["amount", "base", "date", "rates"]
    missing = [field for field in required if field not in data]
    passed = len(missing) == 0
    return {
        "name": "Required fields present",
        "status": "PASS" if passed else "FAIL",
        "details": "missing=" + ", ".join(missing) if missing else "all fields present",
        "latency_ms": response["latency_ms"],
    }


def test_field_types(response):
    data = response["json"] or {}
    passed = (
        isinstance(data.get("amount"), (int, float)) and
        isinstance(data.get("base"), str) and
        isinstance(data.get("date"), str) and
        isinstance(data.get("rates"), dict)
    )
    return {
        "name": "Field types valid",
        "status": "PASS" if passed else "FAIL",
        "details": "type check performed",
        "latency_ms": response["latency_ms"],
    }


def test_base_currency_eur(response):
    data = response["json"] or {}
    passed = data.get("base") == "EUR"
    return {
        "name": "Base currency is EUR",
        "status": "PASS" if passed else "FAIL",
        "details": f"base={data.get('base')}",
        "latency_ms": response["latency_ms"],
    }


def test_rates_not_empty(response):
    data = response["json"] or {}
    rates = data.get("rates", {})
    passed = isinstance(rates, dict) and len(rates) > 0
    return {
        "name": "Rates not empty",
        "status": "PASS" if passed else "FAIL",
        "details": f"rates_count={len(rates) if isinstance(rates, dict) else 0}",
        "latency_ms": response["latency_ms"],
    }


def test_usd_rate_positive(response):
    data = response["json"] or {}
    rates = data.get("rates", {})
    usd = rates.get("USD")
    passed = isinstance(usd, (int, float)) and usd > 0
    return {
        "name": "USD rate is positive",
        "status": "PASS" if passed else "FAIL",
        "details": f"USD={usd}",
        "latency_ms": response["latency_ms"],
    }


def test_date_format(response):
    data = response["json"] or {}
    date_value = data.get("date", "")
    passed = bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_value))
    return {
        "name": "Date format YYYY-MM-DD",
        "status": "PASS" if passed else "FAIL",
        "details": f"date={date_value}",
        "latency_ms": response["latency_ms"],
    }
