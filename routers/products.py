from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404:{"message": "No encontrado"}})

class Product(BaseModel):
    id: int
    name: str
    tipo: str
    precio: float

products_list = [Product(id = 1, name = "producto1", tipo = "tipo A", precio = 33.44),
                  Product(id = 2, name = "producto2", tipo = "tipo B", precio = 10.44),
                  Product(id = 3, name = "producto3", tipo = "tipo C", precio = 11.02),
                  Product(id = 4, name = "producto4", tipo = "tipo D", precio = 40.50),
                  Product(id = 5, name = "producto5", tipo = "tipo E", precio = 5.10),]


@router.get("/", status_code=202)
async def products():
    return ["producto1", "producto2", "producto3", "producto4", "producto5"]

@router.get("/{id}")
async def products(id: int):
    return search_products(id)

def search_products(id: int):
    products = filter(lambda product: product.id == id, products_list)
    try:    
        return list(products)[0]
    except:
        return {"error": "No se ha encontrado el producto"}
