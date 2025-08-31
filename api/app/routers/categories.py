from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import CategoryIn, CategoryOut
from ..deps import get_current_user

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    return db.query(models.Category).filter(models.Category.user_id==current.id).all()

@router.post("", response_model=CategoryOut)
def create_category(data: CategoryIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    cat = models.Category(user_id=current.id, name=data.name, type=models.CategoryType(data.type))
    db.add(cat); db.commit(); db.refresh(cat)
    return cat
