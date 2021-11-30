from crear import crear_notas
from model import modelo

notas_de_venta = 2000
productos = 25000

print("iniciando!")
df_notas = crear_notas(notas_de_venta,productos)
print(df_notas)

model = modelo(df_notas)