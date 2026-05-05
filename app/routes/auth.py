from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.database import SessionLocal
from app.models.user import User
from app.jwt import create_access_token
from app.dependencies import get_current_user

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == req.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        username=req.username,
        password=hash_password(req.password),
        role=req.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()

    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user
