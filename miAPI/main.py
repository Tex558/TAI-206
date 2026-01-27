#importaciones
from fastapi import FastAPI

#Inicializacion del servidor
app= FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenido a tu API REST"}