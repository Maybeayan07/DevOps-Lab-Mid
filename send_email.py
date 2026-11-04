import os
import json
import smtplib
from pathlib import Path
from email.message import EmailMessage

BASE_DIR = Path(__file__).parent
REPORT_FILE = BASE_DIR / "test-report.json"

GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not GMAIL_USERNAME or not GMAIL_APP_PASSWORD:
    raise ValueError("Gmail credentials are missing from GitHub Secrets.")

if not REPORT_FILE.exists():
    raise FileNotFoundError("test-report.json was not generated.")

with open(REPORT_FILE, "r", encoding="utf-8") as file:
    report = json.load(file)

status = report["status"].upper()

message = EmailMessage()
message["Subject"] = f"DevOps Lab CI Test Report - {status}"
message["From"] = GMAIL_USERNAME
message["To"] = GMAIL_USERNAME

message.set_content(
    f"""DevOps Lab Mid Assignment - CI Test Report

Repository: {report['repository']}
Branch: {report['branch']}
Commit: {report['commit_sha']}
GitHub Actions Run ID: {report['run_id']}

Total Tests: {report['total']}
Passed: {report['passed']}
Failed: {report['failed']}
Skipped: {report.get('skipped', 0)}

Overall Status: {status}

The detailed JSON test report is attached.
"""
)

with open(REPORT_FILE, "rb") as file:
    message.add_attachment(
        file.read(),
        maintype="application",
        subtype="json",
        filename="test-report.json"
    )

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
    server.send_message(message)

print(f"Email report sent successfully. Status: {status}")