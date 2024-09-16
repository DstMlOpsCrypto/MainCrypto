from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extras import RealDictCursor
from ..database import get_db
from ..authentification.security import get_current_user, User
from pydantic import BaseModel
from typing import List

# Création d'un routeur FastAPI
router = APIRouter()

class Asset(BaseModel):
    id: int
    asset: str
    symbol: str
    exchange: str

@router.get("/assets", response_model=List[Asset])
async def get_all_assets(current_user: User = Depends(get_current_user)):
    async with get_db() as db:
        try:
            db.execute("SELECT id, asset, symbol, exchange FROM assets")
            assets = db.fetchall()
            return [Asset(**asset) for asset in assets]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

