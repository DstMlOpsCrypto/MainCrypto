from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
    User,
    Token,
)
# Importation de la base de données fictive
# il faudra changer cette base de données pour une base de données réelle quand disponible
from .database import fake_users_db 
####

# Création d'un routeur FastAPI
router = APIRouter()

# Définition d'un modèle Pydantic pour la création d'un nouvel utilisateur
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

# Route pour l'inscription (signup)
@router.post("/signup", response_model=User)
async def signup(user: UserCreate, current_user: User = Depends(get_current_user)):
    # Vérification que seul un admin peut créer de nouveaux comptes
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create new accounts")
    # Vérification que le nom d'utilisateur n'est pas déjà utilisé
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Hachage du mot de passe
    hashed_password = get_password_hash(user.password)
    # Ajout de l'utilisateur à la base de données fictive
    fake_users_db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": "user",
    }
    # Retourne l'utilisateur créé
    return fake_users_db[user.username]

# Route pour la connexion (login)
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Recherche de l'utilisateur dans la base de données fictive
    user = fake_users_db.get(form_data.username)
    # Vérification que l'utilisateur existe et que le mot de passe est correct
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Création d'un token d'accès
    access_token = create_access_token(data={"sub": user["username"]})
    # Retourne le token d'accès
    return {"access_token": access_token, "token_type": "bearer"}

# Route pour lire les informations de l'utilisateur actuel
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user