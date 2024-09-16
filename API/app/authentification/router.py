from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..database import get_db
from .utils import get_password_hash, verify_password
from datetime import timedelta
from .security import create_access_token, get_current_user, oauth2_scheme, ACCESS_TOKEN_EXPIRE_MINUTES, User
from typing import List, Optional

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create new accounts")
    
    async with get_db() as db:
        db.execute("SELECT * FROM members WHERE username = %s", (user.username,))
        if db.fetchone():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        
        hashed_password = get_password_hash(user.password)
        db.execute(
            "INSERT INTO members (username, email, hashed_password, role) VALUES (%s, %s, %s, %s) RETURNING *",
            (user.username, user.email, hashed_password, user.role)
        )
        new_user = db.fetchone()
        db.connection.commit()
        return {"message": f"User {user.username} created successfully", "user": new_user}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with get_db() as db:
        db.execute("SELECT * FROM members WHERE username = %s", (form_data.username,))
        user = db.fetchone()
        
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"], "scopes": [user["role"]]},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer", role=user["role"])

@router.get("/protected", response_model=dict, dependencies=[Depends(oauth2_scheme)])
async def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user": current_user.username,
        "role": current_user.role
    }

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/validate")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        user = await get_current_user(token)
        return {"valid": True, "username": user.username, "role": user.role}
    except HTTPException:
        return {"valid": False}

@router.put("/users/me", response_model=User)
async def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    async with get_db() as db:
        update_fields = []
        update_values = []
        
        if user_update.username and user_update.username != current_user.username:
            db.execute("SELECT * FROM members WHERE username = %s", (user_update.username,))
            if db.fetchone():
                raise HTTPException(status_code=400, detail="Username already taken")
            update_fields.append("username = %s")
            update_values.append(user_update.username)
        
        if user_update.email:
            update_fields.append("email = %s")
            update_values.append(user_update.email)
        
        if user_update.password:
            hashed_password = get_password_hash(user_update.password)
            update_fields.append("hashed_password = %s")
            update_values.append(hashed_password)
        
        if update_fields:
            update_query = f"UPDATE members SET {', '.join(update_fields)} WHERE username = %s RETURNING *"
            update_values.append(current_user.username)
            db.execute(update_query, tuple(update_values))
            updated_user = db.fetchone()
            db.connection.commit()
            return User(**updated_user)
        else:
            return current_user

@router.delete("/users/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this account")
    
    async with get_db() as db:
        db.execute("DELETE FROM members WHERE username = %s", (username,))
        if db.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        db.connection.commit()
    return {"message": "User deleted successfully"}

@router.put("/users/{username}/role", response_model=User)
async def update_user_role(username: str, role_update: UserRoleUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can change user roles")
    
    async with get_db() as db:
        db.execute("UPDATE members SET role = %s WHERE username = %s RETURNING *", (role_update.role, username))
        updated_user = db.fetchone()
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        db.connection.commit()
        return User(**updated_user)

@router.get("/users", response_model=List[User])
async def get_all_users(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view all users")
    
    async with get_db() as db:
        db.execute("SELECT * FROM members")
        users = db.fetchall()
        return [User(**user) for user in users]