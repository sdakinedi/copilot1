from fastapi.testclient import TestClient

import src.app as app_module


def test_root_redirect():
    # Arrange
    client = TestClient(app_module.app)

    # Act
    resp = client.get("/", allow_redirects=False)

    # Assert
    assert resp.status_code in (307, 302)
    assert resp.headers.get("location") == "/static/index.html"
