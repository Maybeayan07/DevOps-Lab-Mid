
import pytest
from app import app, submissions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    submissions.clear()

    with app.test_client() as test_client:
        yield test_client

    submissions.clear()


def test_valid_submission(client):
    response = client.post("/", data={
        "name": "Test Student",
        "reg_no": "FA23-BAI-027",
        "title": "DevOps Lab Mid",
        "submission_url": "https://github.com"
    })

    assert response.status_code == 302
    assert len(submissions) == 1
    assert submissions[0]["reg_no"] == "FA23-BAI-027"

    response = client.get("/")
    assert b"Test Student" in response.data


def test_missing_registration_number(client):
    response = client.post("/", data={
        "name": "Test Student",
        "reg_no": "",
        "title": "DevOps Lab Mid",
        "submission_url": "https://github.com"
    })

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(submissions) == 0


def test_invalid_submission_url(client):
    response = client.post("/", data={
        "name": "Test Student",
        "reg_no": "FA23-BAI-027",
        "title": "DevOps Lab Mid",
        "submission_url": "not-a-valid-url"
    })

    assert response.status_code == 200
    assert b"Please enter a valid HTTP or HTTPS URL." in response.data
    assert len(submissions) == 0
