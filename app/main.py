from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine
from app.models.user import User  

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
