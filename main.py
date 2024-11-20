from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = 'ticket.jpg'

img = Image.open(image_path)

text = pytesseract.image_to_string(img, lang = 'spa')

with open("salida.txt", "w", encoding="utf-8") as file:
    file.write(text)


