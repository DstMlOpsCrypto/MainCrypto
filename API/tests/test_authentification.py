from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_login(client: TestClient, fake_users):
    with patch('app.authentification.router.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_db.fetchone.return_value = fake_users["admin"]
        mock_get_db.return_value.__aenter__.return_value = mock_db

        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "admin"}
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "role" in response.json()
        assert response.json()["role"] == "admin"

def test_signup(client: TestClient, admin_token, fake_users):
    with patch('app.authentification.router.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_db.fetchone.return_value = None
        mock_get_db.return_value.__aenter__.return_value = mock_db

        response = client.post(
            "/auth/signup",
            json={
                "username": "test",
                "email": "tes@test.com",
                "password": "test",
                "role": "admin"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        assert response.status_code == 201
        assert "message" in response.json()
        assert "user" in response.json()

def test_protected_route(client: TestClient, user_token):
    response = client.get(
        "/auth/protected",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
    assert "message" in response.json()
    assert "user" in response.json()
    assert "role" in response.json()