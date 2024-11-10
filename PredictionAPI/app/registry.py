from prometheus_client import CollectorRegistry, Counter, Histogram, Gauge

# Créer un registre Prometheus global
registry = CollectorRegistry()

# Définir les métriques globales
REQUEST_COUNT = Counter('prediction_api_request_count', 'Total number of requests', registry=registry)
REQUEST_LATENCY = Histogram('prediction_api_request_latency_seconds', 'Request latency', registry=registry)
EXCEPTION_COUNT = Counter('prediction_api_exception_count', 'Total number of exceptions', registry=registry)
PREDICTION_COUNT = Counter('prediction_api_prediction_count', 'Total number of predictions made', registry=registry)
MODEL_SCORE = Gauge('prediction_api_model_score', 'Score of the latest model', registry=registry)