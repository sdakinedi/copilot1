import urllib.parse

from fastapi.testclient import TestClient

import src.app as app_module


def _quote(name: str) -> str:
    return urllib.parse.quote(name, safe="")


def test_get_activities():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("Chess Club")
    email = "test_signup@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("Chess Club")
    existing = app_module.activities["Chess Club"]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": existing})

    # Assert
    assert resp.status_code == 400


def test_signup_not_found():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("No Such Activity")

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": "a@b.com"})

    # Assert
    assert resp.status_code == 404


def test_unregister_success():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("Chess Club")
    email = app_module.activities["Chess Club"]["participants"][0]

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("Chess Club")

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": "not@here.com"})

    # Assert
    assert resp.status_code == 400


def test_unregister_not_found():
    # Arrange
    client = TestClient(app_module.app)
    activity = _quote("No Such Activity")

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": "a@b.com"})

    # Assert
    assert resp.status_code == 404
