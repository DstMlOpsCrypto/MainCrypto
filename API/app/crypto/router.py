from fastapi import APIRouter, Depends, HTTPException, Query, status
from psycopg2.extras import RealDictCursor
from ..database import get_db
from ..authentification.security import get_current_user, User
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import httpx


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

class OHLCData(BaseModel):
    asset: str
    dtutc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    trades: float

@router.get("/asset_history/{asset}", response_model=List[OHLCData])
async def get_asset_history(
    asset: str,
    start_date: Optional[datetime] = Query(None, description="Start date for filtering data"),
    end_date: Optional[datetime] = Query(None, description="End date for filtering data"),
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Number of records to return"),
    current_user: User = Depends(get_current_user)
):
    async with get_db() as db:
        try:
            query = "SELECT * FROM ohlc WHERE asset = %s"
            params = [asset]

            if start_date:
                query += " AND dtutc >= %s"
                params.append(start_date)
            if end_date:
                query += " AND dtutc <= %s"
                params.append(end_date)

            query += " ORDER BY dtutc DESC"
            if limit:
                query += " LIMIT %s"
                params.append(limit)

            db.execute(query, tuple(params))
            history = db.fetchall()
            return [OHLCData(**record) for record in history]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class AssetCreate(BaseModel):
    asset: str
    symbol: str
    exchange: str

@router.post("/assets", response_model=Asset, status_code=status.HTTP_201_CREATED)
async def create_asset(asset: AssetCreate, current_user: User = Depends(get_current_user)):
    async with get_db() as db:
        try:
            query = "INSERT INTO assets (asset, symbol, exchange) VALUES (%s, %s, %s) RETURNING id, asset, symbol, exchange"
            db.execute(query, (asset.asset, asset.symbol, asset.exchange))
            new_asset = db.fetchone()
            db.connection.commit()
            
            # Trigger the Airflow DAG using the API
            airflow_api_url = "http://airflow-webserver:8080/api/v1/dags/fetch_historical_ohlc/dagRuns"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Basic YWlyZmxvdzphaXJmbG93"  # Base64 encoded "airflow:airflow"
            }
            payload = {
                "conf": {"asset": asset.asset},
                "dag_run_id": f"manual__{datetime.now().isoformat()}"
            }
            
            response = requests.post(airflow_api_url, json=payload, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Failed to trigger Airflow DAG: {response.text}")
            
            return Asset(**new_asset)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(asset_id: int, current_user: User = Depends(get_current_user)):
    async with get_db() as db:
        try:
            query = "DELETE FROM assets WHERE id = %s"
            db.execute(query, (asset_id,))
            db.connection.commit()
            if db.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asset not found")
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class KrakenAsset(BaseModel):
    asset: str
    symbol: str
    exchange: str = "kraken"
    base: str
    quote: str
    status: str

#Kraken API Assets
@router.get("/kraken_assets", response_model=List[KrakenAsset])
async def get_kraken_assets(current_user: User = Depends(get_current_user)):
    url = "https://api.kraken.com/0/public/AssetPairs"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Kraken API")
    
    data = response.json()
    
    if "result" not in data:
        raise HTTPException(status_code=500, detail="Unexpected response format from Kraken API")
    
    assets = []
    for key, value in data["result"].items():
        asset = KrakenAsset(
            asset=key,
            symbol=value["altname"],
            exchange="kraken",
            base=value["base"],
            quote=value["quote"],
            status=value["status"]
        )
        assets.append(asset)
    
    return assets



