from motor import motor_asyncio

# MongoDB setup
client = motor_asyncio.AsyncIOMotorClient("mongodb+srv://lifogira:lifogira@dynamometer.jm7ru.mongodb.net/?retryWrites=true&w=majority&appName=Dynamometer")
database = client.Main
user_collection = database.User 
patient_data_collection = database.PatientData 