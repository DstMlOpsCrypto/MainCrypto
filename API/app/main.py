import sys
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Importe les routeurs 
from app.auth.router import router as auth_router
from app.ml.router import router as ml_router

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Route racine
@app.get("/")

@limiter.limit("5/minute")
async def home(request: Request):
    return {"message": "Welcome to the API"}

# Inclut les routeurs dans l'application
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ml_router, prefix="/ml", tags=["ml"])