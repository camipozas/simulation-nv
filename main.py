from crear import crear_notas
from model import modelo
from decorator import mide_tiempo


@mide_tiempo
def main():
    notas_de_venta = 2000
    productos = 25000
    print("iniciando!")
    df_notas = crear_notas(notas_de_venta, productos)
    print(df_notas)

    return modelo(df_notas)


modelo = main()
