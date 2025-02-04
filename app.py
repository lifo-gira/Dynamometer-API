from typing import List
from fastapi import  FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import user_collection,patient_data_collection

from models import PatientData, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Message": "use '/docs' endpoint to find all the api related docs "}

@app.post("/login")
async def login(user: User):
    # Retrieve user from MongoDB based on the provided email
    db_user = await user_collection.find_one({"email": user.email})
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the password matches
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return {"message": "Login successful", "username": db_user["username"]}

@app.post("/register")
async def register(user: User):
    # Check if the email is already registered
    existing_user = await user_collection.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user data in MongoDB with plain text password
    await user_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": user.password  # Store plain text password
    })
    
    return {"message": "User registered successfully"}

@app.post("/patient-data")
async def post_patient_data(patient_data: PatientData):
    # Check if the email is already used in the collection
    existing_patient = await patient_data_collection.find_one({"email": patient_data.email})
    
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered with a patient")
    
    # Insert the patient data into the database
    result = await patient_data_collection.insert_one(patient_data.dict())
    
    return {"message": "Patient data successfully added"}

@app.get("/patient-data", response_model=List[PatientData])
async def get_patient_data(email: str):
    if email:
        # If email is provided, search for the patient by email
        patient = await patient_data_collection.find_one({"email": email})
        if patient:
            return [PatientData(**patient)]  # Return as a list
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
    else:
        # If no email is provided, retrieve all patients
        patients_cursor = patient_data_collection.find({})
        patients = [PatientData(**patient) for patient in await patients_cursor.to_list(length=100)]  # Adjust length as needed
        return patients

