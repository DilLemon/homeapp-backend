from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Numeric, Text
from .database import Base
import enum

class CategoryType(str, enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True, nullable=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    pass_hash = Column(String(256), nullable=False)
    role = Column(String(32), default="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    currency = Column(String(8), default="RUB")
    balance_start = Column(Numeric(14,2), default=0)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    type = Column(Enum(CategoryType), nullable=False)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    amount = Column(Numeric(14,2), nullable=False)
    currency = Column(String(8), default="RUB")
    happened_at = Column(Date, nullable=False)
    note = Column(Text)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    amount_planned = Column(Numeric(14,2), nullable=False)

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(128), nullable=False)
    periodicity = Column(String(32), default="daily")
    target_per_period = Column(Integer)

class HabitEntry(Base):
    __tablename__ = "habit_entries"
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Integer, default=1)
    comment = Column(Text)

class RecurringTx(Base):
    __tablename__ = "recurring_transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    amount = Column(Numeric(14,2), nullable=False)
    currency = Column(String(8), default="RUB")
    periodicity = Column(String(32), default="monthly")
    next_date = Column(Date)
    note = Column(Text)
