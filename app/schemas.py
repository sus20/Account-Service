import uuid

from pydantic import BaseModel


class Account(BaseModel):
    id: str = str(uuid.uuid4())
    firstName: str
    lastName: str
    accountNumber: int
