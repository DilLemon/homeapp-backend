from sqlalchemy.orm import Session
from . import models
from .security import hash_password
from .config import settings

EXPENSES = [
    "Алкоголь","Здоровье, красота, гигиена","Кино, театры, музеи","Одежда","Подарки",
    "Продукты","Прочее","Рестораны","Связь","Творчество, книги, обучение",
    "Транспорт","Кредит","ЖКХ","Еда в офисе","Накопления","Фастфуд",
    "Бензин","Бытовуха","Штрафы","Платные дороги","Wildberries","Ozon","Яндекс Маркет",
    "Парковка","Техника"
]
INCOMES = [
    "Аванс","Зарплата","Премия","Дивиденды","Отпускные","Кэшбэк",
    "Возврат долга","Выплата по командировке","Wildberries"
]

HABITS = ["Чтение","Заполнение бюджета","Внесение калорий"]

def ensure_seed(db: Session):
    if not db.query(models.User).count():
        u1 = models.User(username="erik", pass_hash=hash_password(settings.ERIK_PASSWORD))
        u2 = models.User(username="polina", pass_hash=hash_password(settings.POLINA_PASSWORD))
        db.add_all([u1,u2])
        db.flush()
        a1 = models.Account(user_id=u1.id, name="Карта", currency="RUB", balance_start=0)
        a2 = models.Account(user_id=u2.id, name="Карта", currency="RUB", balance_start=0)
        db.add_all([a1,a2])
        db.flush()
        for uid in (u1.id, u2.id):
            db.add_all([models.Category(user_id=uid, name=n, type=models.CategoryType.expense) for n in EXPENSES])
            db.add_all([models.Category(user_id=uid, name=n, type=models.CategoryType.income) for n in INCOMES])
        for uid in (u1.id, u2.id):
            for h in HABITS:
                db.add(models.Habit(user_id=uid, title=h, periodicity="daily"))
        db.commit()
