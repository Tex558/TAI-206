from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status,HTTPException,Depends
import secrets
#Seguridad de HTTPBasic

security= HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username,"emilianojc")
    contraAuth = secrets.compare_digest(credentials.password,"12345")
    
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas"
        )

    return credentials.username
