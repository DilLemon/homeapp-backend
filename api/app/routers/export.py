from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from io import StringIO, BytesIO
import pandas as pd
from ..database import get_db
from .. import models
from ..deps import get_current_user
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/csv")
def export_csv(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    q = db.query(models.Transaction).filter(models.Transaction.user_id==current.id).all()
    rows = [
        {
            "id": t.id,
            "account_id": t.account_id,
            "category_id": t.category_id,
            "amount": float(t.amount),  # type: ignore[arg-type]
            "currency": t.currency,
            "happened_at": t.happened_at.isoformat(),
            "note": t.note or "",
        } for t in q
    ]
    csv_io = StringIO()
    pd.DataFrame(rows).to_csv(csv_io, index=False)
    csv_io.seek(0)
    return StreamingResponse(iter([csv_io.getvalue()]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=transactions.csv"})

@router.get("/xlsx")
def export_xlsx(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):  # type: ignore[type-arg]
    q = db.query(models.Transaction).filter(models.Transaction.user_id==current.id).all()
    rows = [
        {
            "id": t.id,
            "account_id": t.account_id,
            "category_id": t.category_id,
            "amount": float(t.amount),  # type: ignore[arg-type]
            "currency": t.currency,
            "happened_at": t.happened_at.isoformat(),
            "note": t.note or "",
        } for t in q
    ]
    xls_io = BytesIO()
    with pd.ExcelWriter(xls_io, engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(writer, index=False, sheet_name="Transactions")
    xls_io.seek(0)
    return StreamingResponse(xls_io, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition":"attachment; filename=transactions.xlsx"})
