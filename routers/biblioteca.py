from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# En este diccionario definimos los usuarios con códigos de token que existen en nuestra biblioteca
# que pueden conllevar multa o no:
MULTAS_DB = {"token_juan": 0, "token_maria": 15, "token_pepe": 0, "token_lucas": 10}

# Defino esquema de seguridad:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función de dependencia:
async def validar_prestamo(token: str = Depends(oauth2_scheme)):
    if token not in MULTAS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado para sacar libros",
            headers={"WWW-Authenticate": "Bearer"}
        )
    multa = MULTAS_DB[token]
    if multa>0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No puedes pedir libros prestados hasta pagar tu multa de {multa}€"
        )
    return token


@app.get("/pedir-libro")
async def pedir_libro(token: str = Depends(validar_prestamo)):
    return{"mensaje": "Libro prestado con éxito", "usuario token: ": token}
            


