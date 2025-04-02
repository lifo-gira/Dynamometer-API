from pydantic import BaseModel, EmailStr
from typing import Literal, Optional, List, Dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    type: Literal["patient", "therapist"]

    class Config:
        schema_extra = {
            "example": {
                "type": "patient",
                "email": "APM@gmail.com",
                "password": "21345"
            }
        }
    

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "APM",
                "email": "APM@gmail.com",
                "password": "21345",
            }
        }

class ExerciseRecord(BaseModel):
    total_muscles: int
    device_name: str
    date: str
    individual_reps: Dict[str, Dict[str, List[float]]]  # Rep group -> Muscle name -> Graph values

class PatientData(BaseModel):
    user_id: str
    username: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    dob: Optional[str] = None
    blood_grp: Optional[str] = None
    flag: int 
    height: Optional[int] = None
    weight: Optional[int] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    exerciseRecord: Optional[List[ExerciseRecord]] = None  # List of exercise records (indexed)

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
                "flag": 1,
                "exerciseRecord": [
                    {
                        "total_muscles": 50,
                        "device_name": "Dynamometer",
                        "date": "2024-08-22",
                        "individual_reps": {
                            "rep 1": {
                                "Biceps": [10, 12, 8],
                                "Triceps": [15, 14, 13],
                                "Forearm": [7, 9, 11]
                            },
                            "rep 2": {
                                "Biceps": [10, 12, 8],
                                "Triceps": [15, 14, 13],
                                "Forearm": [7, 9, 11]
                            }
                        }
                    },
                    {
                        "total_muscles": 50,
                        "device_name": "Dynamometer",
                        "date": "2024-08-22",
                        "individual_reps": {
                            "rep 1": {
                                "Biceps": [10, 12, 8],
                                "Triceps": [15, 14, 13],
                                "Forearm": [7, 9, 11]
                            },
                            "rep 2": {
                                "Biceps": [10, 12, 8],
                                "Triceps": [15, 14, 13],
                                "Forearm": [7, 9, 11]
                            }
                        }
                    }
                ]
            }
        }