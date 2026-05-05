from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.leave import LeaveRequest
from app.schemas.leave import LeaveCreate
from app.auth import get_current_user  # we assume you already have JWT working

router = APIRouter(prefix="/leave", tags=["Leave"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 1. Employee: create leave request
@router.post("/request")
def create_leave(
    req: LeaveCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    leave = LeaveRequest(
        user_id=user.id,
        reason=req.reason,
        start_date=req.start_date,
        end_date=req.end_date,
        status="pending"
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {"message": "Leave request submitted", "id": leave.id}


# 🔹 2. Employee: view own leaves
@router.get("/my")
def my_leaves(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    leaves = db.query(LeaveRequest).filter(LeaveRequest.user_id == user.id).all()
    return leaves


# 🔹 3. Employer: view all leaves
@router.get("/all")
def all_leaves(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(LeaveRequest).all()


# 🔹 4. Employer: approve/reject
@router.post("/{leave_id}/action")
def update_leave(
    leave_id: int,
    action: str,  # "approved" or "rejected"
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Not allowed")

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if action not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid action")

    leave.status = action
    leave.approved_by = user.id

    db.commit()
    db.refresh(leave)

    return {"message": f"Leave {action}"}
