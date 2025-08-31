from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    class Config:
        from_attributes = True

class LoginIn(BaseModel):
    username: str
    password: str

class AccountIn(BaseModel):
    name: str
    currency: str = "RUB"
    balance_start: float = 0

class AccountOut(AccountIn):
    id: int
    class Config:
        from_attributes = True

class CategoryIn(BaseModel):
    name: str
    type: str  # income|expense

class CategoryOut(CategoryIn):
    id: int
    class Config:
        from_attributes = True

class TransactionIn(BaseModel):
    account_id: int
    category_id: int
    amount: float
    currency: str = "RUB"
    happened_at: date
    note: Optional[str] = None

class TransactionOut(TransactionIn):
    id: int
    class Config:
        from_attributes = True

class HabitIn(BaseModel):
    title: str
    periodicity: str = "daily"
    target_per_period: Optional[int] = None

class HabitOut(HabitIn):
    id: int
    class Config:
        from_attributes = True

class HabitEntryIn(BaseModel):
    date: date
    value: int = 1
    comment: Optional[str] = None

class HabitEntryOut(HabitEntryIn):
    id: int
    class Config:
        from_attributes = True

class ReportSpendingItem(BaseModel):
    category: str
    total: float

class ReportTrendItem(BaseModel):
    period: str
    income: float
    expense: float
