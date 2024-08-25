from fastapi.testclient import TestClient

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

# This test function checks if the get current user process works correctly
def test_get_current_user(client: TestClient, user_token: str):
    response = client.get(
        "/auth/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    # Check if the get current user was successful (status code 200), good username
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
