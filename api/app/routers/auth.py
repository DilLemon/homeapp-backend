from typing import cast
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..security import verify_password
from ..jwt_utils import create_access_token
from ..schemas import LoginIn, Token, UserOut
from ..deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, cast(str, user.pass_hash)):  # type: ignore[arg-type]
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(cast(str, user.username))  # type: ignore[arg-type]
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    return current
