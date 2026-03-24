from sqlalchemy import Column, String, Integer
from app.data.db import Base

class Usuario(Base): 
    __tablename__ = "tb_usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)
    