import os
from dotenv import load_dotenv, find_dotenv

path = find_dotenv()
if path:
    load_dotenv(path)

database_path = os.getenv("DATABASE_PATH", "webring.db")
webring_name = os.getenv("WEBRING_NAME", "Webring")
public_url = os.getenv("PUBLIC_URL", "http://127.0.0.1:5000")
password = os.getenv("PASSWORD", "abc123")
jwt_secret = os.getenv("JWT_SECRET")
jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")