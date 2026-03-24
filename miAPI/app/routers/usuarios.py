
from fastapi import status, HTTPException,Depends, APIRouter 
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB


router= APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)

@router.get("/")
async def consultaUsuarios(db:Session= Depends(get_db)):
    
    conusuarios= db.query(UsuarioDB).all()
    
    return{
        "status":"200",
        "total": len(conusuarios),
        "data":conusuarios
    }

@router.post("/")
async def agregar_usuarios(usuario:UsuarioBase,db:Session= Depends(get_db)):
    
    nuevoUsuario=UsuarioDB(nombre= usuario.nombre, edad= usuario.edad)
    
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    
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