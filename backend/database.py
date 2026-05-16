from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy.sql import func

# NOTA: Deixa 'db' se fores testar com o teu docker-compose local, 
# ou altera para 'gym-db' se fores rodar no Ansible do Jenkins.
DATABASE_URL = "postgresql://postgres:janeiro2004@db:5432/GymApp"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Tabela de Membros alinhada com as necessidades do main.py
class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    plan = Column(String, nullable=False) # Ex: Mensal, Anual
    status = Column(String, default="active") # active / inactive

# Tabela de Checkins alinhada com as necessidades do main.py
class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id", ondelete="CASCADE"))
    checkin_date = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(String, default="Main Gym")
    checked_out = Column(DateTime, nullable=True) # Para o método checkout()

# Função obrigatória para o Depends(get_db) do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()