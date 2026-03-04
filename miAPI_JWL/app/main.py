# Importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
import asyncio
import jwt
import datetime

# Inicialización o instancia de la API
app = FastAPI(
    title='Mi primer API',
    description='Emiliano Jimenez Cantu',
    version='1.0'
)

usuarios = [
    {"id": 1, "nombre": "Saúl", "edad": 24},
    {"id": 2, "nombre": "Lalo", "edad": 21},
    {"id": 3, "nombre": "Mau", "edad": 21},
]

# Modelo de validación Pydantic
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121")

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/token")

SECRET_KEY = "12345"
ALGORITHM = "HS256"

# Función para generar el token
def crear_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data.update({"exp": expiration})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Función para verificar el token
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido",
        )

# Endpoints

# Endpoint de inicio
@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Hola mundo FastAPI "}

# Endpoint de bienvenida
@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST "}

# Endpoint asincrónico de calificaciones
@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "calificación en TAI es 7 "}

# Endpoint de consulta con parámetro obligatorio
@app.get("/v1/parametroO/{id}", tags=['Parametro obligatorio'])
async def consultaUsuarios(id: int):
    await asyncio.sleep(3)
    return {"usuario encontrado": id}

# Endpoint de consulta con parámetro opcional
@app.get("/v1/ParametroOp/", tags=['Parametro opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:  # Se busca usuario en el diccionario de usuarios
            if usuario["id"] == id:
                return {"Usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"AVISO": "No se proporcionó ID"}

# Endpoint para listar todos los usuarios
@app.get("/v1/usuarios/", tags=['CRUD Usuarios'])
async def consultaUsuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# Endpoint para agregar un nuevo usuario
@app.post("/v1/usuarios/", tags=['CRUD Usuarios'])
async def agregar_usuarios(usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario agregado exitosamente",
        "datos": usuario,
        "status": "200"
    }

# Endpoint para actualizar un usuario
@app.put("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def actualizar_usuario(id: int, usuario: dict, token: str = Depends(verificar_token)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx] = {**usr, **usuario}
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usuarios[idx],
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )

# Endpoint para eliminar un usuario
@app.delete("/v1/usuarios/{id}", tags=['CRUD Usuarios'])
async def eliminar_usuario(id: int, token: str = Depends(verificar_token)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            del usuarios[idx]
            return {
                "mensaje": "Usuario eliminado exitosamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="Usuario no encontrado"
    )

# Endpoint para obtener el token
@app.post("/v1/token", tags=['Autenticación'])
async def login(credentials: UsuarioBase):
    # Asegurémonos de que el usuario y la contraseña son correctos (simulado aquí)
    if credentials.nombre == "emiliano" and credentials.id == 1:
        token = crear_token({"sub": credentials.nombre})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )