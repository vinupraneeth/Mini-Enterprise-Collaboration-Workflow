from fastapi import FastAPI

from fastapi_pagination import add_pagination

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.middleware.request_logging_middleware import (
    RequestLoggingMiddleware
)

from app.middleware.rate_limit_middleware import (
    RateLimitMiddleware
)

from app.models import *

from app.db.database import (
    engine,
    Base
)

from app.routers.auth_router import (
    router as auth_router
)

from app.routers.task_router import (
    router as task_router
)

from app.routers.user_router import (
    router as user_router
)

from app.routers.task_comment_router import (
    router as task_comment_router
)

from app.routers.approval_router import (
    router as approval_router
)

from app.routers.activity_router import (
    router as activity_router
)

from app.routers.dashboard_router import (
    router as dashboard_router
)

from app.routers.audit_log_router import (
    router as audit_log_router
)

from app.routers.notification_router import (
    router as notification_router
)

from app.routers.document_router import (
    router as document_router
)

from app.routers.websocket_router import (
    router as websocket_router
)

from app.routers.saas_router import (
    router as saas_router
)

from app.routers.payment_router import (
    router as payment_router
)

#CORS MIDDLEWARE COnFIG for CROSS ORIGIN request handling
app = FastAPI()


app.add_middleware(

    RateLimitMiddleware
)


app.add_middleware(

    RequestLoggingMiddleware
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(auth_router)

app.include_router(task_router)

app.include_router(user_router)

app.include_router(task_comment_router)

app.include_router(approval_router)

app.include_router(activity_router)

app.include_router(dashboard_router)

app.include_router(audit_log_router)

app.include_router(notification_router)

app.include_router(document_router)

app.include_router(websocket_router)

app.include_router(saas_router)

app.include_router(payment_router)

add_pagination(app)
