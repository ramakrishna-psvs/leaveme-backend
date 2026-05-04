from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LeaveMe API running 🚀"}

from app.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.routes import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth")

