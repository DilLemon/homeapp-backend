from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import HabitIn, HabitOut, HabitEntryIn, HabitEntryOut
from ..deps import get_current_user

router = APIRouter(prefix="/api/habits", tags=["habits"])

@router.get("", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    return db.query(models.Habit).filter(models.Habit.user_id==current.id).all()

@router.post("", response_model=HabitOut)
def create_habit(data: HabitIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    h = models.Habit(user_id=current.id, **data.model_dump())
    db.add(h); db.commit(); db.refresh(h)
    return h

@router.post("/{habit_id}/checkins", response_model=HabitEntryOut)
def add_checkin(habit_id: int, data: HabitEntryIn, db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    h = db.get(models.Habit, habit_id)
    if h is None or h.user_id != current.id:
        raise HTTPException(status_code=404, detail="Habit not found")
    e = models.HabitEntry(habit_id=habit_id, **data.model_dump())
    db.add(e); db.commit(); db.refresh(e)
    return e
