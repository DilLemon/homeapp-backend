from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models
from ..schemas import TransactionIn, TransactionOut
from ..deps import get_current_user

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.get("", response_model=list[TransactionOut])
def list_tx(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    return db.query(models.Transaction).filter(models.Transaction.user_id==current.id).order_by(models.Transaction.happened_at.desc()).limit(500).all()

@router.post("", response_model=TransactionOut)
def create_tx(data: TransactionIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    tx = models.Transaction(user_id=current.id, **data.model_dump())
    db.add(tx); db.commit(); db.refresh(tx)
    return tx
