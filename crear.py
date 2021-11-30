import random
import pandas as pd
import numpy as np

def crear_productos():
  data = []
  for i in range(25000):
    valor = random.randint(1,3500) * 100
    data.append([str(i+1), valor])
  return pd.DataFrame(data, columns=["id_prod", "ingreso"])

def crear_inventario():
  data = []
  for i in range(25000):
    valor = random.randint(0,2500)
    data.append([str(i+1), valor])
  return pd.DataFrame(data, columns=["id_prod", "inventario"])

def calc_status(row_existencia):
  if row_existencia > 0:
    row_status = "Y"
  else:
    row_status = "N"
  return row_status

def crear_notas(notas_de_venta,productos):
    df_ingreso = crear_productos()
    df_inventario = crear_inventario()
    df_notas = pd.DataFrame(columns = ['id_nota','id_producto','precio_prod','cantidad', 'inventario', 'existencias','status'])
    tuples = []

    for nota in range(notas_de_venta):
        n_productos = random.randint(1,50)
        productos = random.choices(df_ingreso.to_numpy(), k=n_productos)
        rows = []
        temp_tuples = []
        for producto in productos:
            cantidad = random.randint(1,100)
            row_inventario = df_inventario.loc[int(producto[0])-1]
            existencias = int(row_inventario['inventario']) - int(cantidad)
            status = calc_status(existencias)
            row =  [str(nota + 1), producto[0], producto[1], cantidad, row_inventario['inventario'], existencias, status]
            temp_tuples.append((str(nota + 1), producto[0]))
            rows.append(row)
        temp_tuples.reverse()
        tuples += temp_tuples
        rows = pd.DataFrame(rows, columns=df_notas.columns)
        df_notas = pd.concat([rows, df_notas],  ignore_index=True)
    tuples.reverse()
    index = pd.MultiIndex.from_tuples(tuples, names=["nota", "producto"])
    df_notas.index=index
    return df_notas