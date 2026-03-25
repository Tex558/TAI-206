from fastapi import HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase, UsuarioPatch
from app.security.auth import verificar_Peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD Usuarios"]
)


@router.get("/")
async def Usuarios(db: Session = Depends(get_db)):
    conusuarios = db.query(UsuarioDB).all()

    return {
        "status": "200",
        "total": len(conusuarios),
        "data": conusuarios
    }


@router.get("/{id}")
async def consultar_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "status": "200",
        "data": usuario
    }


@router.post("/")
async def agregar_usuarios(usuario: UsuarioBase, db: Session = Depends(get_db)):
    nuevoUsuario = UsuarioDB(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return {
        "mensaje": "Usuario agregado exitosamente",
        "datos": nuevoUsuario,
        "status": "200"
    }


@router.put("/{id}")
async def actualizar_usuario(id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "datos": usuario_db,
        "status": "200"
    }


@router.patch("/{id}")
async def editar_usuario(id: int, usuario: UsuarioPatch, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if usuario.nombre is not None:
        usuario_db.nombre = usuario.nombre

    if usuario.edad is not None:
        usuario_db.edad = usuario.edad

    db.commit()
    db.refresh(usuario_db)

    return {
        "mensaje": "Usuario editado correctamente",
        "datos": usuario_db,
        "status": "200"
    }


@router.delete("/{id}")
async def eliminar_usuario(
    id: int,
    db: Session = Depends(get_db),
    usuarioAuth: str = Depends(verificar_Peticion)
):
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario_db)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado exitosamente por {usuarioAuth}",
        "status": "200"
    }