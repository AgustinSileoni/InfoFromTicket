from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

class Producto:
    nombre=""
    precio=""
    def __init__(self,nombre,precio):
        self.nombre = nombre
        self.precio = precio
    def mostrar(self):
        print(nombre)
        print(precio)
    

# Configurar el driver de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado
driver.get("https://www.disco.com.ar/almacen")

# Esperar unos segundos para que la página se cargue completamente
time.sleep(60)

# Obtener el HTML de la página después de que el JavaScript ha cargado los datos
soup = BeautifulSoup(driver.page_source, 'html.parser')

lista_productos = []

# Buscar contenedores de productos y extraer precios
productos = soup.find_all("a", class_="vtex-product-summary-2-x-clearLink")
for producto in productos:
    nombre = producto.find("span", class_="vtex-product-summary-2-x-brandName").text.strip()
    
    # Intentar extraer el precio después de cargar el contenido dinámico
    precio = producto.find("div", class_="discoargentina-store-theme-1dCOMij_MzTzZOCohX1K7w")
    if precio:
        precio = precio.text.strip()
    else:
        precio = "Precio no disponible"
    producto = Producto(nombre, precio)
    producto.mostrar()
    lista_productos.append(producto)

#for p in lista_productos:
    #print(p.mostrar())

# Cerrar el navegador
driver.quit()
