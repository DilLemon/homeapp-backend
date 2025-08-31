from datetime import datetime, timedelta
from jose import jwt
from .config import settings

ALGO = "HS256"

def create_access_token(sub: str, minutes: int | None = None) -> str:
    expire = datetime.utcnow() + timedelta(minutes=minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGO)

from jose import JWTError

def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        return None
