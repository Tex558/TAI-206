from fastapi import status, HTTPException,Depends, APIRouter 
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)

@router.get("/")
async def consultaUsuarios():
    
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@router.post("/")
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

@router.put("/{id}")
async def actualizar_usuario(id: int, usuario: dict):
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

@router.delete("/{id}")
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