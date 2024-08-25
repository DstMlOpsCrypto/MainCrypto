import sys
import os
from app.auth.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.security import create_access_token
from app.auth.database import fake_users_db


ACCESS_TOKEN_EXPIRE_MINUTES = 15 
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# This fixture creates a test client for the FastAPI app.
# It can be used in tests to make requests to the app.
@pytest.fixture
def client():
    return TestClient(app)

# This fixture creates an access token for an admin user.
# It can be used in tests that require admin authentication.
@pytest.fixture
def admin_token():
    return create_access_token(
        data={"sub": "admin", "role": "admin"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


# This fixture creates an access token for a test user.
# It can be used in tests that require test user authentication.
@pytest.fixture
def user_token():
    return create_access_token(
        data={"sub": "testuser", "role": "user"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

@pytest.fixture(autouse=True)
def reset_fake_db():
    from app.auth.utils import get_password_hash
    yield
    # Reset the fake database to its original state after each test
    fake_users_db.clear()
    fake_users_db.update({
        "admin": {
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("adminpassword"),
            "role": "admin",
        },
        "testuser": {
            "username": "testuser",
            "email": "testuser@example.com",
            "hashed_password": get_password_hash("testpassword"),
            "role": "user",
        }
    })

