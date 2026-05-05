from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.leave import LeaveRequest
from app.schemas.leave import LeaveCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/leave", tags=["Leave"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 1. Create leave request (Employee)
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

    return {
        "message": "Leave request submitted",
        "leave": {
            "id": leave.id,
            "status": leave.status
        }
    }


# 🔹 2. Get my leaves (Employee)
@router.get("/my")
def my_leaves(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.user_id == user.id
    ).all()

    return [
        {
            "id": l.id,
            "reason": l.reason,
            "start_date": l.start_date,
            "end_date": l.end_date,
            "status": l.status
        }
        for l in leaves
    ]


# 🔹 3. Get all leaves (Employer)
@router.get("/all")
def all_leaves(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Not allowed")

    leaves = db.query(LeaveRequest).all()

    return [
        {
            "id": l.id,
            "user_id": l.user_id,
            "reason": l.reason,
            "status": l.status
        }
        for l in leaves
    ]


# 🔹 4. Approve / Reject leave (Employer)
@router.post("/{leave_id}/action")
def update_leave(
    leave_id: int,
    action: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Not allowed")

    leave = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if action not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid action")

    leave.status = action
    leave.approved_by = user.id

    db.commit()
    db.refresh(leave)

    return {
        "message": f"Leave {action}",
        "id": leave.id,
        "status": leave.status
    }
