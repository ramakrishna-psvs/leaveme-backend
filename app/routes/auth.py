from fastapi import APIRouter
from app.auth import hash_password, verify_password
from app.database import SessionLocal
from app.models.user import User

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, role: str):
    db = SessionLocal()

    user = User(
        username=username,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

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
