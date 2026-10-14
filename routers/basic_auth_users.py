from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordBearer - Forma en que nos vamos a logar
# OAuth2PasswordRequestForm - Forma en que se envían a nuestra API los criterios de autenticación,

app = FastAPI()

# Criterio de autenticación:
oAuth2 = OAuth2PasswordBearer(tokenUrl="login")
# tokenUrl - URL que se encarga de gestionar la autenticación.

# Como siempre con esto ya tenemos la posibilidad de arrancar la instancia de nuestra API

# A continuación tenemos el usuario que viaja por Web
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# A continuación el usuario de BBDD que hereda del anterior
class UserBD(User):
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
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Una vez que en el usuario se ha autenticado correctamente y nos devuelve el access_token
# tenemos que validar si ese access token es correcto y como estamos utilizando el sistema
# de autenticación OAuth2PasswordBearer, sabemos que lo que siempre tenemos que esperar es un
# token por lo que este current_user de a continuación tiene que tener un token de tipo string
# que tendrá una dependencia que tendremos que buscar dentro de nuestro sistema de autenticación
# y de esta manera ya podemos acceder al token:

async def current_user(token: str = Depends(oAuth2)):
    user = search_user(token) # A ver si encontramos al usuario que tenga ese token
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Credenciales de autenticación inválidas", 
            headers={"WWW-Authenticate":"Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    return user

    
# Implementamos la operación de autenticación
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): # Enviamos el usuario y la contraseña
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="La contraseña no es correcta")

    return{"access_token": user.username, "token_type": "bearer"}

# Una vez autenticados creamos una operción que me dé datos de usuarios
@app.get("/users/me")
async def me(user: User = Depends(current_user)): # Hay un criterio de dependencia que significa que podemos implementar operaciones que validen esta firma.
    return user # Devolverá el usuario si el usuario cumple con el criterio de dependecia en la función current_user

