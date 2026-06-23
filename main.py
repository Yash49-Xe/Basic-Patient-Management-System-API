from fastapi import FastAPI
import json

app = FastAPI(title="Patients Management System API")

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def status():
    return "OK"

@app.get("/view")
def view_patients():
    patients = load_data()
    return patients

@app.get("/view/{id}")
def view_id(id: str):
    patients = load_data()
    if id in patients:
        return {id: patients[id]}
    return {"error": f"Patient {id} does not exist."}