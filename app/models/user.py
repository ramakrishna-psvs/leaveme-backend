from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Leaves created by this user
    leaves = relationship(
        "LeaveRequest",
        foreign_keys="LeaveRequest.user_id",
        back_populates="user"
    )

    # Leaves approved by this user (employer side)
    approved_leaves = relationship(
        "LeaveRequest",
        foreign_keys="LeaveRequest.approved_by",
        back_populates="approver"
    )