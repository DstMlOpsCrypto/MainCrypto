# tests/api/test_auth.py

from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import pytest

app = FastAPI()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str
    role: str

# Base de données fictive
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": "fakehashedadminpassword",
        "role": "admin",
    },
    "testuser": {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedtestpassword",
        "role": "user",
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_verify_password(plain_password: str, hashed_password: str):
    return hashed_password == fake_hash_password(plain_password)

def fake_decode_token(token):
    # Décode le token
    user = fake_users_db.get(token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
        )
    return User(**user)

@router.post("/auth/signup")
async def signup(user: User, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create new accounts")
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = fake_hash_password(user.username + "password")
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }
    return {"message": f"User {user.username} created successfully"}

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or not fake_verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": user_dict["username"], "token_type": "bearer", "role": user_dict["role"]}

@router.get("/auth/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user": current_user.username,
        "role": current_user.role
    }

app.include_router(router)

# Début des tests
client = TestClient(app)

def test_login():
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "user"

def test_protected_route():
    # Obtenir le token
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]

    # Accéde à la route protégée
    response = client.get("/auth/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == "testuser"
    assert data["role"] == "user"

def test_signup():
    # Connexion en tant qu'admin pour créer un nouvel utilisateur
    response = client.post("/auth/login", data={"username": "admin", "password": "adminpassword"})
    token = response.json()["access_token"]

    # Création d'un nouvel utilisateur
    new_user = {
        "username": "newuser",
        "email": "newuser@example.com",
        "role": "user"
    }
    response = client.post("/auth/signup", json=new_user, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == f"User {new_user['username']} created successfully"

def test_signup_non_admin():
    # Connexion en tant qu'utilisateur non-admin
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]

    # Tentative de création d'un nouvel utilisateur
    new_user = {
        "username": "anotheruser",
        "email": "anotheruser@example.com",
        "role": "user"
    }
    response = client.post("/auth/signup", json=new_user, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Only admins can create new accounts"
