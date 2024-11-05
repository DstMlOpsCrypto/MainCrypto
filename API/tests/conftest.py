import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.authentification.security import create_access_token
from datetime import timedelta

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def admin_token():
    return create_access_token(
        data={"sub": "admin", "scopes": ["admin"]},
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def user_token():
    return create_access_token(
        data={"sub": "user", "scopes": ["user"]},
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def fake_users():
    return {
        "admin": {
            "username": "admin",
            "email": "admin@admin.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$U2qt1XoPYSxFyPn/fy8FgA$2xQ08S6Nq2dez3i0b9en6tAO55aHTe4y6jvg3RqPUr4",
            "role": "admin"
        },
        "user": {
            "username": "user",
            "email": "user@user.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$DGEs5ZyTsnZuDcH4X+v9Xw$hXkcx5V+RA8IlZ3TBMK2Yz/kO9mbGljBQqKRvK8CaOQ",
            "role": "user"
        }
    }