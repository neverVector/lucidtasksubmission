from fastapi import Depends
from app.auth import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db

def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user