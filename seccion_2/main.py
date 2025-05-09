from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from typing import List

from libs.NaturalNumber import NaturalSet100

app = FastAPI()

natural_set_instance = NaturalSet100()

class ExtractRequest(BaseModel):
    number: conint(strict= True, gt= 0, le=100) # type: ignore


@app.post("/extract/")
def extract_number(data: ExtractRequest):
    try:
        natural_set_instance.extract(data.number)
        return {"message": f"Número {data.number} extraído correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/missing/")
def get_missing_number():
    try:
        missing = natural_set_instance.get_missing_number()
        return {"missing_number": missing}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/available_numbers/")
def get_available_numbers():
    try:
        available = natural_set_instance.get_available_numbers()
        return {"available_number":available}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))