from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
from .security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
    User,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
# Importation de la base de données fictive
# il faudra changer cette base de données pour une base de données réelle quand disponible
from .database import fake_users_db 
from datetime import timedelta
####

# Création d'un routeur FastAPI
router = APIRouter()

# Définition d'un modèle Pydantic pour la création d'un nouvel utilisateur
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Définition de oauth2_scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Route pour l'inscription (signup)
@router.post("/signup", response_model=User)
async def signup(user: UserCreate, current_user: User = Depends(get_current_user)):
    # Vérification que seul un admin peut créer de nouveaux comptes
    if current_user.role != "admin":
        #raise HTTPException(status_code=403, detail="Only admins can create new accounts")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create new accounts")
    # Vérification que le nom d'utilisateur n'est pas déjà utilisé
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    # Hachage du mot de passe
    hashed_password = get_password_hash(user.password)
    # Ajout de l'utilisateur à la base de données fictive
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": "user",
    }
    fake_users_db[user.username] = new_user
    # Retourne l'utilisateur créé
    return User(**new_user)

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

    # Création d'un token d'accès avec expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", role=user["role"])

# Route pour lire les informations de l'utilisateur actuel
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Route pour la validation du token
@router.post("/validate")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        user = await get_current_user(token)
        return {"valid": True, "username": user.username, "role": user.role}
    except HTTPException:
        return {"valid": False}


############################################################
# Modèle pour la mise à jour de l'utilisateur
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

# Route pour mettre à jour les informations de l'utilisateur
@router.put("/users/me", response_model=User)
async def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    if user_update.username and user_update.username != current_user.username:
        if user_update.username in fake_users_db:
            raise HTTPException(status_code=400, detail="Username already taken")
        fake_users_db[user_update.username] = fake_users_db.pop(current_user.username)
        current_user.username = user_update.username
    
    if user_update.email:
        current_user.email = user_update.email
    
    if user_update.password:
        fake_users_db[current_user.username]["hashed_password"] = get_password_hash(user_update.password)
    
    fake_users_db[current_user.username].update(current_user.dict(exclude={"hashed_password"}))
    return User(**fake_users_db[current_user.username])

# Route pour supprimer le compte de l'utilisateur
@router.delete("/users/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this account")
    
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del fake_users_db[username]
    return {"message": "User deleted successfully"}

# Route pour mettre à jour le rôle d'un utilisateur
class UserRoleUpdate(BaseModel):
    role: str

@router.put("/users/{username}/role", response_model=User)
async def update_user_role(username: str, role_update: UserRoleUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can change user roles")
    if username not in fake_users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    fake_users_db[username]["role"] = role_update.role
    return User(**fake_users_db[username])

@router.get("/users", response_model=List[User])
async def get_all_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all users")
    return list(fake_users_db.values())