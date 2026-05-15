from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Member, Checkin, Base
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.sql import func

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class MemberCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    plan: str

class CheckinCreate(BaseModel):
    member_id: int

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    plan: Optional[str] = None
    status: Optional[str] = None

# --- Members ---
@app.get("/members")
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@app.post("/members")
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.query(Checkin).filter(Checkin.member_id == member_id).delete()

    db.delete(member)
    db.commit()
    return {"message": "Deleted"}

# --- Checkins ---
@app.get("/checkins")
def get_checkins(db: Session = Depends(get_db)):
    return db.query(Checkin).all()

@app.post("/checkins")
def create_checkin(checkin: CheckinCreate, db: Session = Depends(get_db)):
    db_checkin = Checkin(**checkin.dict())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin

@app.put("/members/{member_id}")
def update_member(member_id: int, updates: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in updates.dict(exclude_none=True).items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member

@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    total_members = db.query(Member).count()
    active_members = db.query(Member).filter(Member.status == "active").count()
    inactive_members = db.query(Member).filter(Member.status == "inactive").count()
    total_checkins = db.query(Checkin).count()
    active_checkins = db.query(Checkin).filter(Checkin.checked_out == None).count()
    return {
        "total_members": total_members,
        "active_members": active_members,
        "inactive_members": inactive_members,
        "total_checkins": total_checkins,
        "currently_in_gym": active_checkins
    }

@app.put("/checkins/{checkin_id}/checkout")
def checkout(checkin_id: int, db: Session = Depends(get_db)):
    checkin = db.query(Checkin).filter(Checkin.id == checkin_id).first()
    if not checkin:
        raise HTTPException(status_code=404, detail="Checkin not found")
    if checkin.checked_out:
        raise HTTPException(status_code=400, detail="Already checked out")
    checkin.checked_out = func.now()
    db.commit()
    db.refresh(checkin)
    return checkin