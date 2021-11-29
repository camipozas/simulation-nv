from crear import crear_notas
from model import modelo

notas_de_venta = 1600
productos = 25000

print("iniciando!")
df_notas = crear_notas(notas_de_venta,productos)
display(df_notas)

model = modelo(df_notas)