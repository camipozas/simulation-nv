import random
import pandas as pd
import numpy as np


def crear_productos():
    '''
    Create a dataframe with 25000 rows and two columns, "id_prod" and "ingreso". The values in the
    "ingreso" column are random numbers between 1 and 5000
    :return: A dataframe with two columns, id_prod and ingreso.
    '''
    data = []
    for i in range(25000):
        valor = random.randint(1, 5000) * 100
        data.append([str(i+1), valor])
    return pd.DataFrame(data, columns=["id_prod", "ingreso"])


def crear_inventario():
    '''
    Create a dataframe with 25000 rows and two columns, "id_prod" and "inventario". The values in the
    "inventario" column are random numbers between 0 and 2500
    :return: A dataframe with two columns, id_prod and inventario.
    '''
    data = []
    for i in range(25000):
        valor = random.randint(0, 2500)
        data.append([str(i+1), valor])
    return pd.DataFrame(data, columns=["id_prod", "inventario"])


def calc_status(row_existencia):
    '''
    Calculate the status of a row based on the value of a column

    :param row_existencia: The value of the existencia column in the row you want to evaluate
    :return: The status of the row, either Y or N.
    '''
    if row_existencia > 0:
        row_status = "Y"
    else:
        row_status = "N"
    return row_status


def crear_notas(notas_de_venta, productos):
    '''
    Create a dataframe of notas de venta, with the following columns:

    id_nota, id_producto, precio_prod, cantidad, inventario, existencias, status

    The dataframe should have the following properties:

    - The id_nota column should be the nota number (from 1 to notas_de_venta)
    - The id_producto column should be the producto number (from 1 to n_productos)
    - The precio_prod column should be the price of the producto
    - The cantidad column should be the quantity of the producto
    - The inventario column should be the inventory of the producto
    - The existencias column should be the calculated inventory of the producto after the nota
    - The status column should be the calculated status of the producto after the nota

    The function should return

    :param notas_de_venta: The number of notas de venta you want to create
    :param productos: The number of products you want to create
    :return: A dataframe with the following columns:
        id_nota, id_producto, precio_prod, cantidad, inventario, existencias, status
    '''

    df_ingreso = crear_productos()
    df_inventario = crear_inventario()
    df_notas = pd.DataFrame(columns=[
        'id_nota', 'id_producto', 'precio_prod', 'cantidad', 'inventario', 'existencias', 'status'])
    tuples = []

    for nota in range(notas_de_venta):
        n_productos = random.randint(1, 50)
        productos = random.choices(df_ingreso.to_numpy(), k=n_productos)
        rows = []
        temp_tuples = []
        for producto in productos:
            cantidad = random.randint(1, 100)
            row_inventario = df_inventario.loc[int(producto[0])-1]
            existencias = int(row_inventario['inventario']) - int(cantidad)
            status = calc_status(existencias)
            row = [str(nota + 1), producto[0], producto[1], cantidad,
                   row_inventario['inventario'], existencias, status]
            temp_tuples.append((str(nota + 1), producto[0]))
            rows.append(row)
        temp_tuples.reverse()
        tuples += temp_tuples
        rows = pd.DataFrame(rows, columns=df_notas.columns)
        df_notas = pd.concat([rows, df_notas],  ignore_index=True)
    tuples.reverse()
    index = pd.MultiIndex.from_tuples(tuples, names=["nota", "producto"])
    df_notas.index = index
    return df_notas
