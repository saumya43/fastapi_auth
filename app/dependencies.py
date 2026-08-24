from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database import db
from app.utils.jwt_handler import decode_access_token
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

async def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:
        payload: decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,
                                detail="Invalid token"
                                )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNATHORIZED,
            detail="Invalid or expired token"
        )
    
    try:
        user = await db.database["users"].find_one(
            {"_id":ObjectId(user_id)}
            )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
        