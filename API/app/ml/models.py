from pydantic import BaseModel
from datetime import datetime

# Définition d'un modèle Pydantic pour les données OHLCVT
class OHLCVTData(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: datetime
