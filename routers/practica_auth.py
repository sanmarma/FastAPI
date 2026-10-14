from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# 1. Definimos el diccionario de roles (simulación de BBDD)
ROLES_DB = {
    "admin_token": "Administrador",
    "user_token": "Usuario Normal"
}

# 2. Instancia del guardaespaldas (tokenUrl en minúscula)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 3. Función de Dependencia verificadora
async def obtener_rol(token: str = Depends(oauth2_scheme)):
    if token in ROLES_DB:
        return ROLES_DB[token]  # Devuelve "Administrador" o "Usuario Normal"
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # Constante en MAYÚSCULAS
        detail="Token inexistente",
        headers={"WWW-Authenticate": "Bearer"}
    )

# 4. Endpoint protegido usando la dependencia
@app.get("/mi-rol")
async def ver_mi_rol(rol: str = Depends(obtener_rol)):
    return {"mensaje": "Acceso concedido", "tu_rol": rol}