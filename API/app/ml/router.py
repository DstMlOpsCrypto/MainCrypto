from fastapi import APIRouter, Depends, status
from typing import List
from .models import OHLCVTData
from .database import fetch_ohlcvt_data
from app.auth.security import get_current_user, User
from datetime import timedelta

router = APIRouter()

# Route pour obtenir les données OHLCVT
@router.get("/ohlcvt", response_model=List[OHLCVTData])
def get_ohlcvt_data(current_user: User = Depends(get_current_user)):
    # Check if the user has the necessary role to access this endpoint
    if current_user.role not in ["admin", "user"]:
        # raise HTTPException(status_code=403, detail="Not authorized to access this endpoint")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this endpoint")
    data = fetch_ohlcvt_data()
    return data