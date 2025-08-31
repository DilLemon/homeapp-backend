from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import date
from ..database import get_db
from .. import models
from ..schemas import ReportSpendingItem, ReportTrendItem
from ..deps import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/spending", response_model=list[ReportSpendingItem])
def spending(
    date_from: date | None = None,
    date_to: date | None = None,
    scope: str = Query("mine", enum=["mine","all"]),
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user)  # type: ignore[type-arg]
):
    q = db.query(models.Category.name.label("category"), func.coalesce(func.sum(models.Transaction.amount),0).label("total"))\
        .join(models.Category, models.Transaction.category_id==models.Category.id)\
        .filter(models.Category.type==models.CategoryType.expense)
    if scope == "mine":
        q = q.filter(models.Transaction.user_id==current.id)
    if date_from:
        q = q.filter(models.Transaction.happened_at >= date_from)
    if date_to:
        q = q.filter(models.Transaction.happened_at <= date_to)
    q = q.group_by(models.Category.name).order_by(func.sum(models.Transaction.amount).desc())
    return [ReportSpendingItem(category=r.category, total=float(r.total)) for r in q.all()]

@router.get("/trends", response_model=list[ReportTrendItem])
def trends(
    year: int | None = None,
    scope: str = Query("mine", enum=["mine","all"]),
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user)  # type: ignore[type-arg]
):
    q = db.query(
        func.to_char(models.Transaction.happened_at, 'YYYY-MM').label('period'),
        func.sum(case((models.Category.type==models.CategoryType.income, models.Transaction.amount), else_=0)).label('income'),
        func.sum(case((models.Category.type==models.CategoryType.expense, models.Transaction.amount), else_=0)).label('expense')
    ).join(models.Category, models.Transaction.category_id==models.Category.id)

    if scope == "mine":
        q = q.filter(models.Transaction.user_id==current.id)
    if year:
        q = q.filter(extract('year', models.Transaction.happened_at) == year)

    q = q.group_by('period').order_by('period')
    res = q.all()
    return [ReportTrendItem(period=r.period, income=float(r.income or 0), expense=float(r.expense or 0)) for r in res]
