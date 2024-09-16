from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_get_all_assets(client: TestClient, user_token):
    fake_assets = [
        {"id": 1, "asset": "Bitcoin", "symbol": "BTC", "exchange": "Binance"},
        {"id": 2, "asset": "Ethereum", "symbol": "ETH", "exchange": "Coinbase"}
    ]

    with patch('app.crypto.router.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_db.fetchall.return_value = fake_assets
        mock_get_db.return_value.__aenter__.return_value = mock_db

        response = client.get(
            "/crypto/assets",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["asset"] == "Bitcoin"
        assert response.json()[1]["asset"] == "Ethereum"