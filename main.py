from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from routers import products, users


app = FastAPI()

# Inicia el servidor: uvicorn main:app --reload

# Routers. Tomamos nuestra instancia de api, app e incluimos routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "¡Hola mundo desde FastAPI!"}

@app.get("/usuarios/{usuario_id}")
def read_usuario(usuario_id: int):
    return {"usuario_id": usuario_id, "estado": "activo"}

@app.get("/productos/{categoria}/{producto_id}")
def read_producto(categoria: str, producto_id: int):
    return {
        "categoria": categoria,
        "producto_id": producto_id,
        "disponible": True
    }

@app.get("/buscar_productos/")
def buscar_productos(categoria: str, limite: int = 10):
    return {
        "categoria_buscada": categoria,
        "limite_resultados": limite,
        "mensaje": f"Mostrando hasta {limite} productos de {categoria}"
    }

# Manejo explícito de recursos no encontrados en lógica de negocio
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = None  # Simulación de búsqueda fallida en BD
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El recurso con ID {item_id} no existe en el sistema."
        )
    return item

# NUEVO ENDPOINT: Control de clientes con manejo de errores
@app.get("/clientes/{cliente_id}")
def read_cliente(cliente_id: int):
    if cliente_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID del cliente debe ser un número positivo"
        )
    return {"cliente_id": cliente_id, "nombre": "Cliente de prueba"}