from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from .database import fake_users_db
from .utils import pwd_context, get_password_hash
from .database import fake_users_db


# Secret key for JWT token (in production, store this securely)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360

# Définition du schéma OAuth2 pour la génération de tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")#auth/login


# Définition des modèles Pydantic pour les tokens et les utilisateurs
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str


class User(BaseModel):
    username: str
    email: str
    role: str
    hashed_password: str

# Fonction pour vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour créer un token d'accès
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "role": data.get("role")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour obtenir l'utilisateur actuel à partir du token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décodage du token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Récupération du nom d'utilisateur à partir du token
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        token_data = {"username": username, "role": role}

    except JWTError:
        raise credentials_exception
    # Récupération de l'utilisateur à partir de la base de données fictive (à changer)
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    if user["role"] != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role has changed. Please log in again.",
        )
    return User(**user)