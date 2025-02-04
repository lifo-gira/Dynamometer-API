from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "APM",
                "email": "APM@gmail.com",
                "password": "21345"
            }
        }

class PatientData(BaseModel):
    user_id: str
    username: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    dob: Optional[str] = None
    blood_grp: Optional[str] = None
    flag: bool = True
    height: Optional[int] = None
    weight: Optional[int] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "username": "APM",
                "first_name": "Anirudh",
                "last_name": "Menon",
                "email": "APM@gmail.com",
                "height": 176,
                "weight": 70,
                "dob": "22-08-2024",
                "gender": "male",
                "blood_grp": "O+",
                "phone_number": "28917221",
                "address": "asdsadasds",
                "flag": True
            }
        }
