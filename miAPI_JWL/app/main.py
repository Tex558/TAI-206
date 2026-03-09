# importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Inicialización o instancia de la API
app = FastAPI(
    title='Mi primer API',
    description='Emiliano Jimenez Cantu',
    version='1.0'
)

# BD ficticia
usuarios = [
    {"id": 1, "nombre": "Saúl", "edad": 24},
    {"id": 2, "nombre": "Memi", "edad": 21},
    {"id": 3, "nombre": "Mauchín", "edad": 48},
]

# Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121")


SECRET_KEY = "12345"
ALGORITHM = "HS256"              
EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def crear_token(data: dict):
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    token = jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return usuario
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )



@app.post("/token", tags=['Autenticación'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "ejc" or form_data.password != "12345":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas xdxd"
        )
    token = crear_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola mundo FastAPI "}

@app.get("//v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST "}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "calificacion en TAI es 7 "}

@app.get("/v1/parametroO/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id: int):
    await asyncio.sleep(3)
    return {"usuario encontrado": id}

@app.get("/v1/ParametroOp/", tags=['Parametro opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"AVISO": "No se proporcionó ID"}

@app.get("/v1/usuarios/", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD usuarios'])
async def agregar_usuarios(usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El ID ya existe xd")
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario agregado exitosamente",
        "datos": usuario,
        "status": "200"
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(
    id: int,
    usuario: dict,
    usuarioAuth: str = Depends(verificar_token)
):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": f"Usuario actualizado correctamente por {usuarioAuth}",
                "datos": usuarios[idx],
                "status": "200"
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")


@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_token)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": f"Usuario eliminado exitosamente por {usuarioAuth}",
                "status": "200"
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")