from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. definir la URL de conexion
DATABASE_URL=os.getenv(
    "DATABASE_URL",
    "postgresql://admin:12345@postgres:5432/DB_miapi"
)

#2. crear motor de conexion
engine=create_engine(DATABASE_URL)

#3. agregar gestor de sesiones
sesionlocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

#4. base declarativa para modelos
Base=declarative_base()

#5. funcion para el manejo de sesiones en los request
def get_db():
    db=sesionlocal()
    try:
        yield db
    finally:
        db.close()
