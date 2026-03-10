from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


app = FastAPI(
    title='API Citas medicas',
    description='Examen segundo parcial',
    version='1.0'
)

citas = []


class CitaBase(BaseModel):
    paciente: str = Field(..., min_length=2, max_length=100, description="Nombre del paciente", example="Cien años de soledad")
    doctor: str = Field(..., min_length=2, max_length=100, description="Doctor solicitado", example="Gabriel García Márquez")
    fecha: datetime = Field(..., gt=0, fecha=datetime.now().date, description="Fecha de la cita", example=3-2-2026)
    motivo: str = Field(..., min_length=2, max_length=100, description="Motivo de la cita", example="Gabriel García Márquez")
    estado: bool = Field(default=False, description='Cita confirmada')

class CitaRespuesta(CitaBase):
    id: int = Field(..., gt=0)

def obtener_cita_por_id(cita_id: int):
    return next((cita for cita in citas if cita["id"] == cita_id), None)


@app.post("/v1/citas/", tags=['Citas'], status_code=status.HTTP_201_CREATED, responses={201: {"description": "Cita registrada"}, 400: {"description": "Faltan datos o nombre del libro no válido"}})
async def registrar_cita(cita: CitaBase):
    if any(l["paciente"].strip().lower() == cita.nombre.strip().lower() and l["autor"].strip().lower() == cita.autor.strip().lower() for l in citas):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya fue registrado previamente (mismo nombre y autor)")
    nueva_cita = CitaRespuesta(id=len(citas) + 1, **cita.dict())
    citas.append(nueva_cita.dict())
    return {"mensaje": "Cita registrada correctamente", "status": "201", "data": nueva_cita}


@app.get("/v1/citas/registradas", tags=['Citas'])
async def listar_citas():
    disponibles = [l for l in citas if l["estado"] == "disponible"]
    return {"status": "200", "total": len(citas)}


@app.get("/v1/citas/buscar", tags=['Citas'])
async def buscar_cita(nombre: str):
    termino = nombre.strip().lower()
    if not termino:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del libro no es válido")
    resultados = [l for l in citas if termino in l["paciente"].lower()]
    return {"status": "200", "total": len(resultados), "busqueda": nombre, "data": resultados}
