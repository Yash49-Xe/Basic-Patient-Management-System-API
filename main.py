from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI(title="Patients Management System API")

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

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