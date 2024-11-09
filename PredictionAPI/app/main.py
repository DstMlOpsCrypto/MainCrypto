import logging
from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server, Summary, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


# Import routers
from app.prediction import router as prediction_router

logging.basicConfig(level=logging.DEBUG)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="DstMlOpsCrypto Prediction API",
    description="API for crypto predictions using ML models",
    version="1.0.0",
    openapi_tags=[{"name": "predictions", "description": "Prediction operations"}],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Create Prometheus metrics
REQUEST_COUNT = Counter('prediction_api_request_count', 'Total number of requests')
REQUEST_LATENCY = Histogram('prediction_api_request_latency_seconds', 'Request latency')
EXCEPTION_COUNT = Counter('prediction_api_exception_count', 'Total number of exceptions')

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            EXCEPTION_COUNT.inc()
            raise e

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
@app.get("/")
async def root():
    return {"message": "Welcome to the Prediction API"}

app.include_router(prediction_router.router, prefix="/predict", tags=["predictions"])