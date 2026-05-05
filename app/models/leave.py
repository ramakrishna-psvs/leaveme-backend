from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Who requested the leave
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Who approved the leave (employer)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Leave details
    reason = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Status tracking
    status = Column(String, default="pending")

    # ✅ requester side
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="leaves"
    )

    # ✅ approver side
    approver = relationship(
        "User",
        foreign_keys=[approved_by],
        back_populates="approved_leaves"
    )
