from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Expense(BaseModel):
    amount: float
    category: str
    date: date
    note: str
    

class Budget(BaseModel):
    budget: float


class LoginRequest(BaseModel):
    email: str
    password: str