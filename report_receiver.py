
from flask import Flask, request, jsonify
import json
from pathlib import Path
from datetime import datetime, timezone

app = Flask(__name__)

REPORT_FILE = Path(__file__).parent / "test-report.json"


@app.route("/report", methods=["POST"])
def receive_report():
    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    required_fields = [
        "repository",
        "branch",
        "commit_sha",
        "run_id",
        "timestamp",
        "tests",
        "total",
        "passed",
        "failed",
        "status"
    ]

    missing = [field for field in required_fields if field not in report]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Report received: {report['status']}")
    print(f"Saved to: {REPORT_FILE}")

    return jsonify({
        "message": "Report saved successfully",
        "file": str(REPORT_FILE)
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "receiver running"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
