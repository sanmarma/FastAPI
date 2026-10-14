#Con este módulo muestro todas las variables de entorno de sistema.
import os

for nombre, valor in os.environ.items():
    print(nombre, "=", valor)
