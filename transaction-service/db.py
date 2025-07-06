from sqlalchemy import create_engine, asc, desc, text
from sqlalchemy.orm import sessionmaker, joinedload
from models import Transaction, Contractor, TransactionStatus, SystemAccount
from base import Base
from datetime import datetime

DATABASE_URL = "mysql+mysqlconnector://root:root@mysql/peachtree_bank"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_user_id_by_username(username):
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": username}
        ).first()
        return result[0] if result else None

def get_contractors():
    with SessionLocal() as session:
        return session.query(Contractor).all()

def get_statuses():
    with SessionLocal() as session:
        return session.query(TransactionStatus).all()

def get_system_accounts():
    with SessionLocal() as session:
        return session.query(SystemAccount).all()



def create_transaction(user_id, contractor_id, type, amount, account_id):
    with SessionLocal() as session:
        # Check if account has sufficient balance
        account = session.query(SystemAccount).filter(SystemAccount.id == account_id).first()
        if not account:
            raise ValueError("Account not found")
        
        if float(account.balance) < float(amount):
            raise ValueError("Insufficient balance")
        
        # Get the 'sent' status ID
        sent_status = session.query(TransactionStatus).filter(TransactionStatus.name == 'sent').first()
        if not sent_status:
            raise ValueError("Sent status not found")
        
        # Deduct amount from account balance
        account.balance = float(account.balance) - float(amount)
        
        transaction = Transaction(
            user_id=user_id,
            contractor_id=contractor_id,
            type=type,
            amount=amount,
            status_id=sent_status.id,
            date=datetime.now()
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        
        # Eagerly load the relationships for the response
        return session.query(Transaction).options(joinedload(Transaction.contractor), joinedload(Transaction.status)).filter(Transaction.id == transaction.id).first()

def list_transactions(sort_by='date', sort_order='desc', search=None):
    with SessionLocal() as session:
        query = session.query(Transaction).options(joinedload(Transaction.contractor), joinedload(Transaction.status))
        
        if search:
            query = query.join(Contractor).filter(Contractor.name.ilike(f"%{search}%"))
        if sort_by == 'date':
            query = query.order_by(desc(Transaction.date) if sort_order == 'desc' else asc(Transaction.date))
        elif sort_by == 'contractor':
            query = query.join(Contractor).order_by(asc(Contractor.name) if sort_order == 'asc' else desc(Contractor.name))
        elif sort_by == 'amount':
            query = query.order_by(desc(Transaction.amount) if sort_order == 'desc' else asc(Transaction.amount))
        return query.all()

def get_transaction_by_id(transaction_id):
    with SessionLocal() as session:
        return session.query(Transaction).options(joinedload(Transaction.contractor), joinedload(Transaction.status)).filter(Transaction.id == transaction_id).first()

def update_transaction_status(transaction_id, new_status_id):
    with SessionLocal() as session:
        # Use raw SQL to update the status because of ORM foreign key error
        result = session.execute(
            text("UPDATE transactions SET status_id = :status_id WHERE id = :transaction_id"),
            {"status_id": new_status_id, "transaction_id": transaction_id}
        )
        session.commit()
        
        # Return the updated transaction using ORM for the response
        return session.query(Transaction).options(joinedload(Transaction.contractor), joinedload(Transaction.status)).filter(Transaction.id == transaction_id).first() 