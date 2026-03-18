from pydantic import BaseModel, Field

#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id:int = Field(...,gt=0,description="Identificador de usuario", example="1")
    nombre:str = Field(...,min_length=3, max_length= 50, description="Nombre del usuario")
    edad:int = Field(...,ge=0, le=121, description= "Edad válida entre 0 y 121")
