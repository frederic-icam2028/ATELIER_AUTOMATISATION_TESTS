from flask import Flask, render_template, jsonify
from tester.runner import run_all_tests
from storage import init_db, save_run, list_runs

app = Flask(__name__)

init_db()


@app.get("/")
def consignes():
    return render_template("consignes.html")


@app.get("/run")
def run():
    result = run_all_tests()
    save_run(result)
    return jsonify(result)


@app.get("/dashboard")
def dashboard():
    runs = list_runs()
    latest = runs[0] if runs else None
    return render_template("dashboard.html", latest=latest, runs=runs)


@app.get("/health")
def health():
    runs = list_runs()

    if not runs:
        return jsonify({
            "status": "unknown",
            "message": "No runs yet"
        })

    latest = runs[0]
    global_status = "healthy" if latest["summary"]["failed"] == 0 else "degraded"

    return jsonify({
        "status": global_status,
        "last_run": latest["timestamp"],
        "passed": latest["summary"]["passed"],
        "failed": latest["summary"]["failed"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
