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

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7"
    )
)

PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "PASSWORD_RESET_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)

GOOGLE_OAUTH_CLIENT_ID = os.getenv(
    "GOOGLE_OAUTH_CLIENT_ID",
    ""
)

GOOGLE_OAUTH_CLIENT_SECRET = os.getenv(
    "GOOGLE_OAUTH_CLIENT_SECRET",
    ""
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

CACHE_DEFAULT_TTL_SECONDS = int(
    os.getenv(
        "CACHE_DEFAULT_TTL_SECONDS",
        "300"
    )
)

RAZORPAY_KEY_ID = os.getenv(
    "RAZORPAY_KEY_ID",
    ""
)

RAZORPAY_KEY_SECRET = os.getenv(
    "RAZORPAY_KEY_SECRET",
    ""
)
