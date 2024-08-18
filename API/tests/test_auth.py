from fastapi.testclient import TestClient
from app.auth.database import fake_users_db

# This test function checks if the signup process works correctly
def test_signup(client: TestClient, admin_token: str):
    response = client.post(
        "/auth/signup",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    # Check if the signup was successful (status code 200), good username, good role
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["role"] == "user"

# This test function checks if the login process works correctly
def test_login(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "adminpassword"}
    )
    # Check if the login was successful (status code 200), and if the access token is in the response
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "role" in response.json()
    assert "token_type" in response.json()

# This test function checks if the get current user process works correctly
def test_get_current_user(client: TestClient, user_token: str):
    response = client.get(
        "/auth/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    # Check if the get current user was successful (status code 200), good username
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_validate_token(client: TestClient, user_token: str):
    response = client.post(
        "/auth/validate",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["valid"] == True
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"

def test_update_user(client: TestClient, user_token: str):
    response = client.put(
        "/auth/users/me",
        json={"email": "newemail@example.com"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newemail@example.com"

def test_delete_user(client: TestClient, admin_token: str):
    response = client.delete(
        "/auth/users/testuser",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"

def test_update_user_role(client: TestClient, admin_token: str):
    response = client.put(
        "/auth/users/testuser/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    # Manually update the fake database
    fake_users_db["testuser"]["role"] = "admin"

def test_get_all_users(client: TestClient, admin_token: str):
    response = client.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Negative test cases
def test_signup_non_admin(client: TestClient, user_token: str):
    response = client.post(
        "/auth/signup",
        json={
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password": "newpassword2"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

def test_update_user_role_non_admin(client: TestClient, user_token: str):
    response = client.put(
        "/auth/users/testuser/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

def test_get_all_users_non_admin(client: TestClient, user_token: str):
    response = client.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403