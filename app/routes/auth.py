from fastapi import APIRouter
from app.auth import hash_password, verify_password
from app.database import SessionLocal
from app.models.user import User

router = APIRouter()

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str

@router.post("/register")
def register(req: RegisterRequest):
    req.username
    req.password
    req.role

    return {"message": "User created successfully"}

@router.post("/login")
def login(username: str, password: str):
    db = SessionLocal()

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    return {
        "message": "Login successful",
        "role": user.role
    }
