from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from models import User, RefreshToken

DATABASE_URL = "mysql+mysqlconnector://root:root@mysql/peachtree_bank"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_user_by_username(username):
    with SessionLocal() as session:
        return session.query(User).filter(User.username == username).first()

def create_user(username, password):
    with SessionLocal() as session:
        hashed_pw = bcrypt.hash(password)
        user = User(username=username, password=hashed_pw)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def delete_user(username):
    with SessionLocal() as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            session.delete(user)
            session.commit()

def store_refresh_token(username, token):
    with SessionLocal() as session:
        refresh_token = RefreshToken(username=username, token=token)
        session.add(refresh_token)
        session.commit()

def revoke_refresh_token(token):
    with SessionLocal() as session:
        refresh_token = session.query(RefreshToken).filter(RefreshToken.token == token).first()
        if refresh_token:
            refresh_token.revoked = 1
            session.commit()

def is_refresh_token_revoked(token):
    with SessionLocal() as session:
        refresh_token = session.query(RefreshToken).filter(RefreshToken.token == token).first()
        if refresh_token is None:
            return True  # If not found, treat as revoked
        return bool(refresh_token.revoked) 