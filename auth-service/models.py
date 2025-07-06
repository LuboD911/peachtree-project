from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    token = Column(String(512), nullable=False)
    revoked = Column(Integer, default=0)
    issued_at = Column(DateTime, default=datetime.datetime.utcnow) 