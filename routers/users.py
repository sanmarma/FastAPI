from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Inicia el servidor: uvicorn users:app --reload

# Entidad user

# Al poner BaseModel tiene ya el mecanismo interno para crear el objeto y tratar con él.

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id = 1, name = "Brais", surname = "Moure",url = "https://moure.dev",age = 35),
              User(id = 2, name = "Moure", surname = "Dev",url = "https://mouredev.com",age =35),
              User(id = 3, name = "Pepe", surname = "Jones",url = "https://pepejones.com",age =33)]

async def usersjson():
    return [{"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev", "url": "https://mouredev.com", "age": 35},
            {"name": "Pepe", "surname": "Jones", "url": "https://pepejones.com", "age": 33}]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

@router.get("/userquery/")
async def user(id:int):
    return search_user(id)
    

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:    
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

@router.post("/user", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        #Usando errores propios del http. En lugar de return ponemos mejor raise.
        #En la request me fijo en el label status. raise lo que hace es propagar la excepción
        raise HTTPException(status_code=404, detail = "El usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put("/user")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return user

    if not found:
            return {"error": "No se ha actualizado el ususario"}

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
            if saved_user.id == id:
                found = True
                del users_list[index]
                return users_list
    if not found:
        return {"error": "No se ha eliminado el ususario"}
            


    
  


