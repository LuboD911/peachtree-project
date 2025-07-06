from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from base import Base
import enum

class TransactionTypeEnum(str, enum.Enum):
    card_payment = 'card_payment'
    online_transfer = 'online_transfer'
    transaction = 'transaction'

class TransactionStatus(Base):
    __tablename__ = 'transaction_statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    color = Column(String(20), nullable=False)
    transactions = relationship("Transaction", back_populates="status")

class Contractor(Base):
    __tablename__ = 'contractors'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    image_url = Column(String(512), nullable=False, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    transactions = relationship("Transaction", back_populates="contractor")

class SystemAccount(Base):
    __tablename__ = 'system_accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    balance = Column(DECIMAL(15, 2), nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    type = Column(Enum(TransactionTypeEnum), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status_id = Column(Integer, ForeignKey('transaction_statuses.id'), nullable=False)

    contractor = relationship("Contractor", back_populates="transactions")
    status = relationship("TransactionStatus", back_populates="transactions") 