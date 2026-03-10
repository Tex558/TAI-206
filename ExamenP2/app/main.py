from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


app = FastAPI(
    title='API Citas medicas',
    description='Examen segundo parcial',
    version='1.0'
)

security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username,"root")
    contraAuth = secrets.compare_digest(credentials.password,"1234")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )

    return credentials.username


citas = []


class CitaBase(BaseModel):
    paciente: str = Field(..., min_length=2, max_length=100, description="Nombre del paciente", example="Emiliano Jimenez")
    doctor: str = Field(..., min_length=2, max_length=100, description="Doctor solicitado", example="Saul Silva")
    anio: int = Field(..., gt=2026, le=datetime.now().year, description="Año de la cita", example=2026)
    motivo: str = Field(..., min_length=2, max_length=100, description="Motivo de la cita", example="Gripe leve")
    estado: bool = Field(default=False, description='Cita confirmada')

class CitaRespuesta(CitaBase):
    id: int = Field(..., gt=0)

def obtener_cita_por_id(cita_id: int):
    return next((cita for cita in citas if cita["id"] == cita_id), None)


@app.post("/v1/citas/", tags=['Citas'], status_code=status.HTTP_201_CREATED, responses={201: {"description": "Cita registrada"}, 400: {"description": "Faltan datos"}})
async def registrar_cita(cita: CitaBase):
    if any(l["paciente"].strip().lower() == cita.nombre.strip().lower() and l["autor"].strip().lower() == cita.autor.strip().lower() for l in citas):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya fue registrado previamente (mismo nombre y autor)")
    nueva_cita = CitaRespuesta(id=len(citas) + 1, **cita.dict())
    citas.append(nueva_cita.dict())
    return {"mensaje": "Cita registrada correctamente", "status": "201", "data": nueva_cita}

@app.get("/v1/citas/listadas", tags=['Citas'])
async def listar_citas(usuarioAuth:str = Depends(verificar_Peticion)):
    return {"status": "200", "total": len(citas)}


@app.get("/v1/citas/buscar", tags=['Citas'])
async def buscar_cita(nombre: str):
    termino = nombre.strip().lower()
    if not termino:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del paciente no es válido")
    resultados = [l for l in citas if termino in l["paciente"].lower()]
    return {"status": "200", "total": len(resultados), "busqueda": nombre, "data": resultados}

@app.put("/v1/citas/{id}", tags=['Citas'])
async def confirmar_cita(id: int, cita: dict):
    for idx, conf in enumerate(citas):
        if conf["id"] == id:
            citas[idx] = {**conf, **cita}
            return {
                "mensaje": "Cita confirmada",
                "datos": citas[idx],
                "status": "200"
            }
            
    raise HTTPException(
        status_code=400,
        detail="Cita no encontrada"
        )

@app.delete("/v1/citas/{id}", tags=['Citas'])
async def eliminar_cita(id: int, usuarioAuth:str = Depends(verificar_Peticion)):
    for idx, cit in enumerate(citas):
        if cit["id"] == id:
            del citas[idx]
            return {
                "mensaje": f"Cita eliminada exitosamente",
                "status": "200"
            }
        raise HTTPException(
        status_code=400,
        detail="Cita no encontrada"
        )