from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
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


#CORS MIDDLEWARE COnFIG for CROSS ORIGIN request handling
app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(auth_router)

app.include_router(task_router)

app.include_router(user_router)