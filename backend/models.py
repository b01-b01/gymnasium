from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Member(Base):
    __tablename__ = "members"
    id        = Column(Integer, primary_key=True)
    name      = Column(String(100), nullable=False)
    email     = Column(String(100), unique=True, nullable=False)
    phone     = Column(String(20))
    plan      = Column(String(20), nullable=False)
    status    = Column(String(10), default="active")
    joined_at = Column(DateTime, server_default=func.now())

class Checkin(Base):
    __tablename__ = "checkins"
    id          = Column(Integer, primary_key=True)
    member_id   = Column(Integer, ForeignKey("members.id"))
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"))
    checked_in  = Column(DateTime, server_default=func.now())
    checked_out = Column(DateTime, nullable=True)
