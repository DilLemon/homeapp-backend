from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import AccountIn, AccountOut
from ..deps import get_current_user

router = APIRouter(prefix="/api/accounts", tags=["accounts"])

@router.get("", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    return db.query(models.Account).filter(models.Account.user_id == current.id).all()

@router.post("", response_model=AccountOut)
def create_account(data: AccountIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    acc = models.Account(user_id=current.id, **data.model_dump())
    db.add(acc); db.commit(); db.refresh(acc)
    return acc
