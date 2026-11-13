
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

submissions = []


# --------------------------------
# 1. Validate Assignment Submission
# --------------------------------
def validate_submission(data):

    name = data.get("name", "").strip()
    reg_no = data.get("reg_no", "").strip()
    title = data.get("title", "").strip()
    submission_url = data.get("submission_url", "").strip()

    if not name or not reg_no or not title or not submission_url:
        return False, "All fields are required."

    try:
        parsed_url = urlparse(submission_url)

        # Only HTTP and HTTPS URLs are allowed
        if parsed_url.scheme.lower() not in ("http", "https"):
            return False, "Please enter a valid HTTP or HTTPS URL."

        # Hostname is compulsory
        if not parsed_url.hostname:
            return False, "Please enter a valid HTTP or HTTPS URL."

        # Validate hostname format
        hostname = parsed_url.hostname

        if "." not in hostname:
            return False, "Please enter a valid URL with a domain name."

        if any(char.isspace() for char in hostname):
            return False, "URL cannot contain spaces."

        # Validate malformed port numbers
        _ = parsed_url.port

    except ValueError:
        return False, "Please enter a valid HTTP or HTTPS URL."

    return True, "Submission successful."


# --------------------------------
# 2. Send Email Notification
# --------------------------------
def send_submission_email(submission):

    username = os.getenv("GMAIL_USERNAME", "").strip()
    app_password = os.getenv(
        "GMAIL_APP_PASSWORD", ""
    ).replace(" ", "")

    if not username or not app_password:
        print("GMAIL ERROR: Credentials are missing.")
        return False

    message = EmailMessage()

    message["Subject"] = "New DevOps Lab Submission Received"
    message["From"] = username
    message["To"] = username

    message.set_content(
        f"""
A new student submission has been received.

Student Name: {submission['name']}
Registration Number: {submission['reg_no']}
Assignment Title: {submission['title']}
Submission URL: {submission['submission_url']}

Status: Successfully Submitted.
"""
    )

    try:
        print("Connecting to Gmail SMTP server...")

        with smtplib.SMTP(
            "smtp.gmail.com", 587, timeout=20
        ) as server:

            server.ehlo()
            server.starttls()
            server.ehlo()

            print("Authenticating Gmail account...")

            server.login(username, app_password)
            server.send_message(message)

        print("SUCCESS: Email notification sent.")
        return True

    except smtplib.SMTPException as error:
        print(f"GMAIL SMTP ERROR: {error}")
        return False

    except OSError as error:
        print(f"GMAIL CONNECTION ERROR: {error}")
        return False

    except Exception as error:
        print(f"UNEXPECTED EMAIL ERROR: {error}")
        return False


# --------------------------------
# 3. Home Route
# --------------------------------
@app.route("/", methods=["GET", "POST"])
def index():

    message = ""
    message_type = ""

    if request.method == "POST":

        received_url = request.form.get(
            "submission_url", ""
        ).strip()

        print("\n---------- NEW SUBMISSION ----------")
        print("RECEIVED URL:", repr(received_url))

        valid, validation_message = validate_submission(
            request.form
        )

        print("VALIDATION RESULT:", valid)
        print("VALIDATION MESSAGE:", validation_message)

        # Reject invalid submissions
        if not valid:

            print("SUBMISSION REJECTED.")
            print("------------------------------------\n")

            return render_template(
                "index.html",
                submissions=submissions,
                message=validation_message,
                message_type="error"
            )

        # Create submission only after validation
        submission = {
            "name": request.form["name"].strip(),
            "reg_no": request.form["reg_no"].strip(),
            "title": request.form["title"].strip(),
            "submission_url": received_url
        }

        submissions.append(submission)

        # Send email only for valid submissions
        email_sent = send_submission_email(submission)

        print("EMAIL STATUS:", email_sent)
        print("------------------------------------\n")

        if email_sent:
            return redirect(
                url_for("index", result="success")
            )

        return redirect(
            url_for("index", result="email_failed")
        )

    # Display result messages
    result = request.args.get("result")

    if result == "success":
        message = (
            "Submission successful! "
            "Email notification sent."
        )
        message_type = "success"

    elif result == "email_failed":
        message = (
            "Submission successful, but email notification failed. "
            "Please check Gmail configuration."
        )
        message_type = "error"

    return render_template(
        "index.html",
        submissions=submissions,
        message=message,
        message_type=message_type
    )


# --------------------------------
# 4. Run Application
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
