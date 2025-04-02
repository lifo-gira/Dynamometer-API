from typing import List
from bson import ObjectId
from fastapi import  FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import user_collection,patient_data_collection

from models import ExerciseRecord, LoginRequest, PatientData, User

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
async def login(user: LoginRequest):
    # Retrieve user from MongoDB using email
    db_user = await user_collection.find_one({"email": user.email})

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate password
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "message": "Login successful",
        "username": db_user["username"],
        "type": db_user["type"]  # Added type field
    }

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
        "password": user.password,  # Store plain text password
        "type": user.type  # Added type field
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

@app.get("/patients", response_model=List[User])
async def get_all_patients():
    patients = await user_collection.find({"type": "patient"}).to_list(None)
    
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")

    return patients

@app.get("/getUser/{email}", response_model=User)
async def get_therapist_by_email(email: str):
    therapist = await user_collection.find_one({"email": email, "type": "therapist"})
    
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")

    return User(**therapist)



@app.get("/patient-data", response_model=PatientData)
async def get_patient_data(email: str):
    patient = await patient_data_collection.find_one({"email": email})
    if patient:
        return PatientData(**patient)  # Return a single object, not a list
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/upload-exercise/")
async def upload_exercise(email: str, first_name: str, last_name: str, exerciseRecord: List[ExerciseRecord]):
    # Find the patient asynchronously
    patient = await patient_data_collection.find_one({"email": email, "first_name": first_name, "last_name": last_name})

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get existing exercise records
    existing_exercise_records = patient.get("exerciseRecord", [])

    for new_record in exerciseRecord:
        new_record_dict = new_record.dict()  # Convert Pydantic model to dict
        
        # Directly stack the new data without checking for matches
        existing_exercise_records.append(new_record_dict)

    # Update the database with the stacked records
    await patient_data_collection.update_one(
        {"email": email, "first_name": first_name, "last_name": last_name},
        {"$set": {"exerciseRecord": existing_exercise_records}}
    )

    return [
    {
        "message": "Exercise record updated successfully"
    }
]
