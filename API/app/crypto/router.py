from fastapi import Depends, APIRouter
from psycopg2.extras import RealDictCursor
from ..database import get_db

# Création d'un routeur FastAPI
router = APIRouter()

@router.get("/members")
def get_members(db: RealDictCursor = Depends(get_db)):
    db.execute("SELECT * FROM members")
    members = db.fetchall()
    return members