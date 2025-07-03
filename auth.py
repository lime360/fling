import datetime
import jwt
from env import jwt_secret, jwt_algorithm

def generate():
    payload = {
        "sub": "admin",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)

def verify(token):
    try:
        jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        return True
    except:
        return False