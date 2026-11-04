
import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

from datetime import datetime, timezone
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).parent
XML_FILE = BASE_DIR / "pytest-results.xml"


def git_command(*args):
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def get_repository():
    repository = os.getenv("GITHUB_REPOSITORY")

    if repository:
        return repository

    remote = git_command("remote", "get-url", "origin")

    if "github.com" in remote:
        return remote.replace(":", "/").split("github.com/")[-1].removesuffix(".git")

    return "local-repository"


def get_test_results():
    if not XML_FILE.exists():
        return []

    root = ET.parse(XML_FILE).getroot()
    results = []

    for case in root.findall(".//testcase"):
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        if failure is not None:
            result = "failed"
            message = failure.get("message") or failure.text or "Test failed"

        elif error is not None:
            result = "failed"
            message = error.get("message") or error.text or "Test error"

        elif skipped is not None:
            result = "skipped"
            message = skipped.get("message") or "Test skipped"

        else:
            result = "passed"
            message = ""

        results.append({
            "name": f"{case.get('classname', '')}::{case.get('name', '')}",
            "result": result,
            "failure_message": message
        })

    return results


def main():
    print("\nRunning automated tests...\n")

    exit_code = pytest.main([
        "-v",
        f"--junitxml={XML_FILE}",
        "tests/"
    ])

    test_results = get_test_results()

    total = len(test_results)
    passed = sum(t["result"] == "passed" for t in test_results)
    failed = sum(t["result"] == "failed" for t in test_results)
    skipped = sum(t["result"] == "skipped" for t in test_results)

    report = {
        "repository": get_repository(),
        "branch": os.getenv("GITHUB_REF_NAME") or git_command("branch", "--show-current"),
        "commit_sha": os.getenv("GITHUB_SHA") or git_command("rev-parse", "HEAD"),
        "run_id": os.getenv("GITHUB_RUN_ID") or "local-run",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": test_results,
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "status": "passed" if exit_code == 0 else "failed"
    }
    with open(BASE_DIR / "test-report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nSending test report to local receiver...")

    data = json.dumps(report).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:5001/report",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            print(response.read().decode("utf-8"))

    except (urllib.error.URLError, TimeoutError) as error:
        print(f"ERROR: Could not deliver report: {error}")
        return 1

    print(f"\nTotal: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Overall status: {report['status']}")

    return int(exit_code)


if __name__ == "__main__":
    sys.exit(main())
