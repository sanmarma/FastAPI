from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 

app = FastAPI()

# Seguimos teniendo un endpoint que se llama login
oAuth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# A continuación el usuario de BBDD que hereda del anterior
class UserDB(User):
   password: str

# Esto puede hacer las veces de tabla de BBDD donde guardo la contraseña
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Braismoure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2": {
            "username": "mouredev2",
            "full_name": "Braismoure2",
            "email": "braismoure2@mouredev.com",
            "disabled": True,
            "password": "654321"
        }
}

def search_user_db(username: str):
    if username in users_db:
        return UserBD(**users_db[username])
    
# Implementamos la operación de autenticación. Esta función la pillamos de basic_auth_users.py, pero vamos 
# a adaptarla 
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): # Enviamos el usuario y la contraseña
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="La contraseña no es correcta")

    return{"access_token": user.username, "token_type": "bearer"}