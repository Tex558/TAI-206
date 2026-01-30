#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Inicializacion / instancia de la API se accede con /docs y la documentacion para usuarios es /redoc
app= FastAPI(
    title='Mi primer API',
    description='Emiliano Jimenez Cantu - Practica 2',
    version='1.0'
)

usuarios=[
    {"id":1, "nombre":"Emiliano", "edad":21},
    {"id":2, "nombre":"Mau", "edad":21},
    {"id":3, "nombre":"Saul", "edad":24},
]
    
#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenido a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"Tu calificacion en TAI es 10"}

@app.get("/v1/usuarios/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return { "usuario encontrado":id }

@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                 return { "usuario encontrado":id ,"Datos":usuario}
        else:
            return { "Mensaje":"Usuario no encontrado"}
    else: 
        return { "Aviso":"No se proporciono Id"}
