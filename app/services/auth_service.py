from datetime import datetime, timedelta
import jwt

JWT_SECRET = 'SECRET'
ALGORITHM = 'HS256'


def create_token(data: dict, expire_delta=None):
    payload = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    payload.update({'exp': expire})
    return jwt.encode(payload, JWT_SECRET, ALGORITHM)