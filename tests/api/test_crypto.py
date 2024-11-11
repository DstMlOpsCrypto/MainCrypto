# tests/api/test_crypto.py

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List, Optional
import pytest

app = FastAPI()
router = APIRouter()

class Asset(BaseModel):
    id: int
    asset: str
    symbol: str
    exchange: str

# Base de données fictive des actifs
fake_assets_db = []

async def get_current_user():
    # Simule un utilisateur authentifié
    return {"username": "admin", "role": "admin"}

@router.get("/crypto/assets", response_model=List[Asset])
async def get_all_assets(current_user: dict = Depends(get_current_user)):
    return fake_assets_db

@router.post("/crypto/assets", response_model=Asset)
async def create_asset(asset: Asset, current_user: dict = Depends(get_current_user)):
    # Vérifie si l'actif existe déjà
    for existing_asset in fake_assets_db:
        if existing_asset.asset == asset.asset:
            raise HTTPException(status_code=400, detail="Asset already exists in the database")
    fake_assets_db.append(asset)
    return asset

app.include_router(router)

# Début des tests
client = TestClient(app)

def test_create_asset():
    new_asset = {
        "id": 1,
        "asset": "TESTASSET",
        "symbol": "TEST",
        "exchange": "kraken"
    }
    response = client.post("/crypto/assets", json=new_asset)
    assert response.status_code == 200
    data = response.json()
    assert data["asset"] == "TESTASSET"

def test_get_all_assets():
    response = client.get("/crypto/assets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Au moins l'actif créé précédemment
