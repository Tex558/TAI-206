from fastapi import APIRouter 
from app.data.database import usuarios
from typing import Optional
import asyncio

router= APIRouter(
    tags=["Misc"]
)
#Endpoints
@router.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI "}

@router.get("/v1/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST "}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"calificacion en TAI es 7 "}

@router.get("/v1/parametroO/{id}")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}

@router.get("/v1/ParametroOp/")
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios: #Se busca usuario en el diccionario de usuarios
            if usuario["id"]== id:
                return { "Usuario encontrado":id,
                         "Datos": usuario 
                         }
            
        return {"Mensaje":"Usuario no encontrado"}
    
    else: 
        return {"AVISO":"No se proporcionó ID"}
    