from fastapi import FastAPI, HTTPException
from joblib import load
import pandas as pd
from pydantic import BaseModel, ValidationError, Field

# Définir une classe Pydantic pour valider les données d'entrée
class InputData(BaseModel):
    prg: float = Field(description="Valeur pour 'prg'", ge=0)
    pl: float = Field(description="Valeur pour 'pl'", ge=0)
    pr: float = Field(description="Valeur pour 'pr'", ge=0)
    sk: float = Field(description="Valeur pour 'sk'", ge=0)
    ts: float = Field(description="Valeur pour 'ts'", ge=0)
    m11: float = Field(description="Valeur pour 'm11'", ge=0)
    bd2: float = Field(description="Valeur pour 'bd2'", ge=0)
    age: float = Field(description="Valeur pour 'age'", gt=0, le=100)
    insurance: int = Field(description="Valeur pour 'insurance'", ge=0, le=1)

# Charger le modèle entraîné
model = load("best_voting_reduced.joblib")

app = FastAPI()

@app.get("/health")
async def health_check():
    """
    Endpoint pour vérifier l'état du système.
    
    Retourne:
    - 'OK' si tout va bien
    """
    return {"status": "OK"}

@app.post("/predict/patient")
async def predict(input_data: InputData):
    """
    Endpoint pour faire une prédiction avec le modèle de machine learning.
    
    Paramètres:
    - input_data: InputData
    
    Retourne:
    - Un dictionnaire contenant le résultat de la prédiction (0 ou 1)
    """
    try:
        valid_input_data = input_data
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    data = pd.DataFrame([valid_input_data.dict()])
    prediction = model.predict(data)
    result = int(prediction[0])
    return {"malade": result}

@app.get("/")
async def root():
    return {"message": "API de prédiction de maladie"}
