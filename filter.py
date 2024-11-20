import re
import pandas as pd

# Texto extraído del ticket
texto = """
1,0000 u x 2549, 9900 ds
2549,99
Yerba Playadito 5009
1,0000 u x 1499,9900
Detergente Zorro 300 dla
1,0000 u X 1769,9900
Arroz integral Gallo 1769,99
1,0000 u x 999,9900
Esponja Virulana 399,99
1,0000 u x 4099,9900
pan integr c/salvado 4099,99
1,0000 u x 1449,9900

1449 99

Manteca PPremio 1009
1,0000 u x 2700,0000

Jamon cocido

0.225 x 11999,99 2700,00
1,0000 u x 1657,5000

Tybo Las Tres

0,195 x 8499.99 1657,50

subtotal 16727,44
Descuento Manteca PPremio 1009 - 350,00

TUTAR 16377,44
"""

# Expresión regular para capturar nombre del producto y precio
pattern = r"([a-zA-Z\s]+)\s*(\d+,\d+)\s*(?:u|x)\s*(\d+,\d+)"

# Extraer los productos y precios del texto
productos = []
for match in re.findall(pattern, texto):
    nombre_producto = match[0].strip()
    precio_unidad = match[2].replace(",", ".")
    productos.append([nombre_producto, float(precio_unidad)])

# Crear un DataFrame de pandas
df = pd.DataFrame(productos, columns=["Producto", "Precio por unidad (o kg)"])

# Guardar en un archivo Excel
#df.to_excel("productos_ticket.xlsx", index=False)
print("Datos guardados en 'productos_ticket.xlsx'")

print(df)
