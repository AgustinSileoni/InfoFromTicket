import requests
from bs4 import BeautifulSoup

# URL de la tienda online
url = "https://www.disco.com.ar/almacen"

# Hacer la solicitud HTTP
response = requests.get(url)
if response.status_code == 200:
    # Crear el objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar contenedores de productos (esto depende del sitio específico)
    productos = soup.find_all("article", class_="vtex-product-summary-2-x-element")

    for producto in productos:
        # Extraer nombre del producto
        nombre = producto.find("span", class_="vtex-product-summary-2-x-brandName").text.strip()
        
        # Extraer precio del producto
        precio = producto.find("div", class_="discoargentina-store-theme-1dCOMij_MzTzZOCohX1K7w")
        
        
        # Imprimir los detalles del producto
        print(f"Nombre: {nombre}")
        print(f"Precio: {precio}")
        print("------")
else:
    print("Error al acceder a la página:", response.status_code)
