from typing import List
from unittest.mock import MagicMock
from .models import OHLCVTData

# Mock PostgreSQL connection
mock_conn = MagicMock()

# Mock OHLCVT data
mock_ohlcvt_data = [
    OHLCVTData(
        open=100.0,
        high=105.0,
        low=98.0,
        close=102.5,
        volume=1000000,
        timestamp="2023-05-01T10:00:00Z"
    ),
    OHLCVTData(
        open=102.0,
        high=104.0,
        low=100.5,
        close=103.0,
        volume=800000,
        timestamp="2023-05-02T10:00:00Z"
    ),
]

def fetch_ohlcvt_data() -> List[OHLCVTData]:
    # Simulate fetching data from PostgreSQL
    return mock_ohlcvt_data
