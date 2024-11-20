import easyocr
import pandas as pd

reader = easyocr.Reader(['es'])

results = reader.readtext("ticket.png")

df = pd.DataFrame(results, columns=['bbox','text','conf'])

df = df.drop('bbox',axis=1)
df = df.drop('conf',axis=1)
print(df)
df.to_csv("salida.txt", sep='\t', index= False)
