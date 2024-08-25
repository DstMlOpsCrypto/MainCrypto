import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.security import create_access_token

# This fixture creates a test client for the FastAPI app.
# It can be used in tests to make requests to the app.
@pytest.fixture
def client():
    return TestClient(app)

# This fixture creates an access token for an admin user.
# It can be used in tests that require admin authentication.
@pytest.fixture
def admin_token():
    return create_access_token(data={"sub": "admin"})

# This fixture creates an access token for a test user.
# It can be used in tests that require test user authentication.
@pytest.fixture
def user_token():
    return create_access_token(data={"sub": "testuser"})