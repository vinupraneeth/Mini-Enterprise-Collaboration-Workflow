from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://username:password@localhost:3306/workflow_db"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "replace_with_a_secure_secret_key"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)
