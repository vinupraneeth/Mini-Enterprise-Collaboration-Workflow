from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import User
from app.routers.auth_router import router as auth_router

from app.routers.task_router import (
    router as task_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
def root():

    return {
        "message": "Mini Enterprise Workflow API Running"
    }