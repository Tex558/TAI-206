from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


app = FastAPI(
    title='API Biblioteca Digital',
    description='Repaso general FastAPI + Pydantic + Docker + Postman',
    version='1.0'
)

libros = []
prestamos = []


class UsuarioPrestamo(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario", example="Alex Cortazar")
    correo: str = Field(..., min_length=5, max_length=120, description="Correo del usuario", example="alex@correo.com")


class LibroBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del libro", example="Cien años de soledad")
    autor: str = Field(..., min_length=2, max_length=100, description="Autor del libro", example="Gabriel García Márquez")
    anio: int = Field(..., gt=0, le=datetime.now().year, description="Año del libro (>0 y <= año actual)", example=1967)
    paginas: int = Field(..., gt=1, description="Número de páginas, entero positivo mayor a 1", example=417)
    estado: str = Field(default="disponible", description='Estado del libro', example="disponible")


class LibroRespuesta(LibroBase):
    id: int = Field(..., gt=0)


class PrestamoCrear(BaseModel):
    libro_id: int = Field(..., gt=0, description="ID del libro a prestar", example=1)
    usuario: UsuarioPrestamo


def obtener_libro_por_id(libro_id: int):
    return next((libro for libro in libros if libro["id"] == libro_id), None)


def obtener_prestamo_por_id(prestamo_id: int):
    return next((prestamo for prestamo in prestamos if prestamo["id"] == prestamo_id), None)


@app.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED, responses={201: {"description": "Libro registrado"}, 400: {"description": "Faltan datos o nombre del libro no válido"}})
async def registrar_libro(libro: LibroBase):
    if any(l["nombre"].strip().lower() == libro.nombre.strip().lower() and l["autor"].strip().lower() == libro.autor.strip().lower() for l in libros):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya fue registrado previamente (mismo nombre y autor)")
    nuevo_libro = LibroRespuesta(id=len(libros) + 1, **libro.dict())
    libros.append(nuevo_libro.dict())
    return {"mensaje": "Libro registrado correctamente", "status": "201", "data": nuevo_libro}


@app.get("/v1/libros/disponibles", tags=['Libros'])
async def listar_libros_disponibles():
    disponibles = [l for l in libros if l["estado"] == "disponible"]
    return {"status": "200", "total": len(disponibles), "data": disponibles}


@app.get("/v1/libros/buscar", tags=['Libros'])
async def buscar_libro_por_nombre(nombre: str):
    termino = nombre.strip().lower()
    if not termino:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del libro no es válido")
    resultados = [l for l in libros if termino in l["nombre"].lower()]
    return {"status": "200", "total": len(resultados), "busqueda": nombre, "data": resultados}


@app.post("/v1/prestamos/", tags=['Préstamos'], status_code=status.HTTP_201_CREATED, responses={201: {"description": "Préstamo registrado"}, 409: {"description": "Conflict si el libro ya está prestado"}})
async def registrar_prestamo(prestamo: PrestamoCrear):
    libro = obtener_libro_por_id(prestamo.libro_id)
    if libro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    if libro["estado"] == "prestado":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado")
    nuevo_prestamo = {"id": len(prestamos) + 1, "libro_id": libro["id"], "libro_nombre": libro["nombre"], "usuario": prestamo.usuario.dict(), "fecha_prestamo": datetime.now().isoformat(timespec="seconds"), "fecha_devolucion": None, "activo": True}
    prestamos.append(nuevo_prestamo)
    libro["estado"] = "prestado"
    return {"mensaje": "Préstamo registrado correctamente", "status": "201", "data": nuevo_prestamo}


@app.put("/v1/prestamos/{prestamo_id}/devolver", tags=['Préstamos'], responses={200: {"description": "OK al devolver un libro"}, 409: {"description": "Conflict si el registro de préstamo ya no existe"}})
async def marcar_libro_como_devuelto(prestamo_id: int):
    prestamo = obtener_prestamo_por_id(prestamo_id)
    if prestamo is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo ya no existe")
    if not prestamo["activo"]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El préstamo ya fue marcado como devuelto")
    prestamo["activo"] = False
    prestamo["fecha_devolucion"] = datetime.now().isoformat(timespec="seconds")
    libro = obtener_libro_por_id(prestamo["libro_id"])
    if libro:
        libro["estado"] = "disponible"
    return {"mensaje": "Libro marcado como devuelto", "status": "200", "data": prestamo}


@app.delete("/v1/prestamos/{prestamo_id}", tags=['Préstamos'], responses={200: {"description": "Registro de préstamo eliminado"}, 409: {"description": "Conflict si el registro de préstamo ya no existe"}})
async def eliminar_registro_prestamo(prestamo_id: int):
    for idx, prestamo in enumerate(prestamos):
        if prestamo["id"] == prestamo_id:
            if prestamo["activo"]:
                libro = obtener_libro_por_id(prestamo["libro_id"])
                if libro:
                    libro["estado"] = "disponible"
            eliminado = prestamos.pop(idx)
            return {"mensaje": "Registro de préstamo eliminado", "status": "200", "data": eliminado}
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo ya no existe")