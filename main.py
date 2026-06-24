from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="ID of the Patient", example="P001")]
    name : Annotated[str, Field(..., description="Name of the Patient")]
    city : Annotated[str, Field(..., description="City of the Patient")]
    age : Annotated[int, Field(..., gt=0, lt= 120, description="Age of the patient and must be greater than zero")]
    gender : Annotated[Literal["male", "female", "other"], Field(..., description="Gender of the patient")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient (in metres)")] 
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient (in kgs)")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/self.height**2, 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", 'w') as f:
        json.dump(data, f)

app = FastAPI(title="Patients Management System API")

@app.get("/")
def status():
    return {"Status":"OK"}

@app.get("/view")
def view_patients():
    patients = load_data()
    return patients

@app.get("/view/{id}")
def view_id(id: str = Path(..., description="ID of the Patient in DB", example="P001")):
    patients = load_data()
    if id in patients:
        return {id: patients[id]}
    raise HTTPException(status_code=404, detail=f"Patient {id} not found.")

@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description="Sort on the basis of heigh, weight or bmi"),
                  order: str = Query("asc", description="sort in ascending or descending order")):
    valid_fields = ["height","weight","bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid Field. Select from {valid_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=404, detail="Invalid order. Select between 'asc' and 'desc'.")
    
    patients = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(patients.values(), key = lambda x : x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    patients = load_data()

    if patient.id in patients:
        raise HTTPException(status_code=400, detail="Patient already exist.")
    
    patients[patient.id] = patient.model_dump(exclude=['id'])

    save_data(patients)

    return JSONResponse(status_code=201, content={"message" : "Patient created successfully!"})

    