from pulp import *
from decorator import log


@log
def modelo(df_notas):
    '''
    The function takes in a dataframe of the form:

    | id_nota | id_producto | cantidad | inventario | precio_prod |
    |---------|-------------|----------|------------|-------------|
    | 1       | 1           | 10       | 10         | 10          |
    | 1       | 2           | 10       | 10         | 10          |
    | 1       | 3           | 10       | 10         | 10          |
    | 2       | 1           | 10       | 10         | 10          |
    | 2       | 2           | 10       | 10         | 10          |
    | 2       | 3           | 10       | 10         | 10          |

    And returns a dataframe of the form:

    | id_nota | id_producto | cantidad |
    |---------|-------------|----------|
    | 1       | 1           | 10       |

    :param df_notas: The dataframe containing the information of the sales orders
    '''
    # Variables
    cant_unidades = LpVariable.dicts("cant_unidades",
                                     ((id_nota, id_producto)
                                      for id_nota, id_producto in df_notas.index),
                                     lowBound=0,
                                     cat='Integer')

    nota_completa = LpVariable.dicts("nota_completa",
                                     ((id_nota, id_producto)
                                      for id_nota, id_producto in df_notas.index),
                                     cat='Binary')

    nota_modificada = LpVariable.dicts("nota_modificada",
                                       ((id_nota, id_producto)
                                        for id_nota, id_producto in df_notas.index),
                                       cat='Binary')

    # Modelo
    model = LpProblem("Supply-Demand-Problem", LpMaximize)

    # Funcion Objetivo
    model += (lpSum([cant_unidades[id_nota, id_producto] * df_notas.loc[(id_nota, id_producto),
              'precio_prod'].sum() for id_nota, id_producto in df_notas.index])), "obj"

    # Restricciones
    # (1) Inventario disponible:
    model += lpSum([cant_unidades[id_nota, id_producto] - df_notas.loc[(id_nota, id_producto),
                   'inventario'].sum() for id_nota, id_producto in df_notas.index]) <= 0, "c1"

    # (2) La cantidad tiene que ser igual o menor a lo que solicitó el cliente:
    model += lpSum([cant_unidades[id_nota, id_producto] <= nota_completa[id_nota, id_producto] *
                   df_notas.loc[(id_nota, id_producto), 'cantidad'].sum() for id_nota, id_producto in df_notas.index]), "c2"
    model += lpSum([cant_unidades[id_nota, id_producto] <= nota_modificada[id_nota, id_producto] *
                   df_notas.loc[(id_nota, id_producto), 'cantidad'].sum() for id_nota, id_producto in df_notas.index]), "c3"

    # Resuelve
    print("status:", str(LpStatus[model.status]))
    model.solve()
    print("objetivo:", round(value(model.objective)))
