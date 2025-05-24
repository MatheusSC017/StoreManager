import pytest
from fastapi.testclient import TestClient
from app.auth.authentication import auth_required, admin_required
from app.main import app


def override_auth_required():
    return {"user": "1", "username": "username", "access": "Regular"}


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[admin_required] = override_auth_required
    app.dependency_overrides[auth_required] = override_auth_required

    with TestClient(app) as c:
        yield c
