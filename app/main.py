from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine
from app.models.user import User
from app.models.leave import LeaveRequest 
from app.routes import leave
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(leave.router)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
