from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# 1. Definimos el guardaespaldas (indica que el token se obtiene en el endpoint /login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 2. Mostrador de Recepción: Emite el token si la clave es "1234"
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "1234":
        # Devolvemos el token que actuará como "pase de entrada"
        return {"access_token": "super_token_secreto", "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas"
    )

# 3. Función verificadora que usaremos como Dependencia
async def verificar_token(token: str = Depends(oauth2_scheme)):
    if token != "super_token_secreto":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no válido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token

# 4. Endpoint protegido
@app.get("/zona-privada")
async def zona_privada(token_valido: str = Depends(verificar_token)):
    return {"mensaje": "¡Bienvenido a la zona VIP!", "tu_token": token_valido}