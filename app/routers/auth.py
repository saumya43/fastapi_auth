
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db_connection
from app.model.user import UserCreate, UserLogin
from app.utils.password import hash_password
from app.utils.password import verify_password
from app.utils.jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict

router = APIRouter(
    prefix = "/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user(user: UserCreate, db = Depends(get_db_connection)):
    existing_user = await db["users"].find_one(
        {"username":user.username}
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="username already exists")
    
    
    new_user = {
        "username": user.username,
        "email": user.email,
        "password_hash": hash_password(user.password)
}

    result = await db["users"].insert_one(new_user)
    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }
   

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db_connection)):
    #1. find user
    existing_user = await db["users"].find_one({"email": form_data.username})
    if not existing_user:
        raise HTTPException(status_code=401,
                            detail="Invalid email or password")

    #2. verify password
    password_valid = verify_password(
        form_data.password,
        existing_user["password_hash"]
    )
     
    if not password_valid:
        raise HTTPException(status_code=401,
                            detail="Invalid email or password")

    #3 generate JWT 
    access_token = create_access_token(
        {
        "sub": str(existing_user["_id"])
        }
    )


    return{
       "access_token": access_token,
       "token_type": "bearer"
    }

