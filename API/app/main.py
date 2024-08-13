import sys
from fastapi import FastAPI
# Importe les routeurs 
from app.auth.router import router as auth_router
from app.ml.router import router as ml_router

app = FastAPI()

# Route racine
@app.get("/")
async def home():
    return {"message": "Welcome to the API"}

# Inclut les routeurs dans l'application
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ml_router, prefix="/ml", tags=["ml"])