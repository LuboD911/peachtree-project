from pydantic import BaseModel
from datetime import datetime

class ContractorRead(BaseModel):
    id: int
    name: str
    image_url: str

    class Config:
        from_attributes = True

class TransactionStatusRead(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True

class TransactionRead(BaseModel):
    id: int
    user_id: int
    date: datetime
    contractor: ContractorRead
    type: str
    amount: float
    status: TransactionStatusRead

    class Config:
        from_attributes = True 