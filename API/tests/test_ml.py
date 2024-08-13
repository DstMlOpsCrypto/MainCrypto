from fastapi.testclient import TestClient

# This test function checks if authenticated users can access OHLCVT data
def test_get_ohlcvt_data(client: TestClient, user_token: str):
    response = client.get(
        "/ml/ohlcvt",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    # Check if the response status code is 200, and if the response contains data
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "open" in response.json()[0]

# This test function checks if unauthorized users cannot access OHLCVT data
def test_get_ohlcvt_data_unauthorized(client: TestClient):
    response = client.get("/ml/ohlcvt")
    # Check if the response status code is 401 (Unauthorized)
    assert response.status_code == 401
