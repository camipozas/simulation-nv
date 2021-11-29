from crear import crear_notas
from model import modelo

notas_de_venta = 1600
productos = 25000

df_notas = crear_notas(notas_de_venta,productos)
df_notas

model = modelo(df_notas)