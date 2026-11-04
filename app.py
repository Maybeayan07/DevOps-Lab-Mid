
from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)

submissions = []


def validate_submission(data):
    name = data.get("name", "").strip()
    reg_no = data.get("reg_no", "").strip()
    title = data.get("title", "").strip()
    submission_url = data.get("submission_url", "").strip()

    if not name or not reg_no or not title or not submission_url:
        return False, "All fields are required."

    parsed_url = urlparse(submission_url)

    if parsed_url.scheme in ("http", "https") or not parsed_url.netloc:
        return False, "Please enter a valid HTTP or HTTPS URL."

    return True, "Submission successful."


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        valid, message = validate_submission(request.form)

        if valid:
            submissions.append({
                "name": request.form["name"].strip(),
                "reg_no": request.form["reg_no"].strip(),
                "title": request.form["title"].strip(),
                "submission_url": request.form["submission_url"].strip()
            })
            return redirect(url_for("index", success=1))

    if request.args.get("success"):
        message = "Submission successful!"

    return render_template(
        "index.html",
        submissions=submissions,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
