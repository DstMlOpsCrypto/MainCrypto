import sys
import logging
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Importe les routeurs 
from app.authentification.router import router as authentification_router
from app.crypto import router as crypto_router
from app.prediction.router import router as prediction_router

logging.basicConfig(level=logging.DEBUG)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="DstMlOpsCrypto API",
    description="API for DstMlOpsCrypto project",
    version="1.0.0",
    openapi_tags=[{"name": "authentication", "description": "Authentication operations"}],
)

app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": "",
    "clientSecret": ""
}

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Route racine
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

app.include_router(authentification_router, prefix="/auth", tags=["authentication"])
app.include_router(crypto_router.router, prefix="/crypto", tags=["crypto"])
app.include_router(prediction_router, prefix="/prediction", tags=["prediction"])



