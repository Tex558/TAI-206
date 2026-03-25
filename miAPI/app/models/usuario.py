from pydantic import BaseModel, Field
from typing import Optional

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    nombre:str = Field(...,min_length=3, max_length= 50, description="Nombre del usuario")
    edad:int = Field(...,ge=0, le=121, description= "Edad válida entre 0 y 121")

class UsuarioPatch(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
