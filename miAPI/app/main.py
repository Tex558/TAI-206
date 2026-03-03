#importaciones
from typing import Optional
from fastapi import FastAPI,status,HTTPException,Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#Iniciaclización o instancia de la API
app= FastAPI(
    title='Mi primer API',
    description='Emiliano Jimenez Cantu',
    version='1.0'
)

#BD ficticia
usuarios=[
    {"id":1,"nombre":"Saúl","edad":24},
    {"id":2,"nombre":"Lalo","edad":21},
    {"id":3,"nombre":"Mau","edad":21},
]

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de usuario", example="1")
    nombre:str = Field(...,min_length=3, max_length= 50, description="Nombre del usuario")
    edad:int = Field(...,ge=0, le=121, description= "Edad válida entre 0 y 121")

#Seguridad de HTTPBasic

security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username,"emilianojc")
    contraAuth = secrets.compare_digest(credentials.password,"12345")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )

    return credentials.username

#Endpoints
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI "}

@app.get("//v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST "}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":"calificacion en TAI es 7 "}

@app.get("/v1/parametroO/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}

@app.get("/v1/ParametroOp/", tags=['Parametro opcional'])
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
    

@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
             status_code= 400,
             detail= "El ID ya existe xd"
        ) 
    usuarios.append(usuario)
    return{
        "mensaje": "Usuario agregado exitosamente",
        "datos":usuario,
        "status":"200"
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": "Usuario actualizado correctamente xd",
                "datos": usuarios[idx],
                "status": "200"
            }
            
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )

@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_Peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": f"Usuario eliminado exitosamente por {usuarioAuth}",
                "status": "200"
            }
        raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
        )