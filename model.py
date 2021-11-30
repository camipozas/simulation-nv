from pulp import *
from decorator import log

@log
def modelo(df_notas):
    # Variables
    cant_unidades = LpVariable.dicts("cant_unidades",
                                        ((id_nota, id_producto) for id_nota, id_producto in df_notas.index),
                                        lowBound=0,
                                        cat='Integer')

    nota_completa = LpVariable.dicts("nota_completa",
                                        ((id_nota, id_producto) for id_nota, id_producto in df_notas.index),
                                        cat='Binary')

    nota_modificada = LpVariable.dicts("nota_modificada",
                                        ((id_nota, id_producto) for id_nota, id_producto in df_notas.index),
                                        cat='Binary')

    # Modelo
    model = LpProblem("Supply-Demand-Problem", LpMaximize)

    # Funcion Objetivo
    model += (lpSum([cant_unidades[id_nota, id_producto] * df_notas.loc[(id_nota,id_producto),'precio_prod'].sum() for id_nota, id_producto in df_notas.index])), "obj"

    # Restricciones
    # (1) Inventario disponible:
    model += lpSum([cant_unidades[id_nota, id_producto] - df_notas.loc[(id_nota, id_producto), 'inventario'].sum() for id_nota, id_producto in df_notas.index]) <= 0, "c1"

    # (2) La cantidad tiene que ser igual o menor a lo que solicitó el cliente:
    model += lpSum([cant_unidades[id_nota, id_producto] - df_notas.loc[(id_nota, id_producto), 'cantidad'].sum() for id_nota, id_producto in df_notas.index]) <= 0, "c2"
    model += lpSum([cant_unidades[id_nota, id_producto] <=  nota_completa[id_nota, id_producto] * df_notas.loc[(id_nota, id_producto), 'cantidad'].sum() for id_nota, id_producto in df_notas.index]), "c3"
    model += lpSum([cant_unidades[id_nota, id_producto] <=  nota_modificada[id_nota, id_producto] * df_notas.loc[(id_nota, id_producto), 'cantidad'].sum() for id_nota, id_producto in df_notas.index]), "c4" 

    # (3) Si la nota de venta está completa entonces no se modifica:
    #model += lpSum([nota_completa[id_nota, id_producto] <=  1 - nota_modificada[id_nota, id_producto] for id_nota, id_producto in df_notas.index]) 

    # (4)	Si la nota fue modificada, no se realiza nuevamente:
    #model += lpSum([nota_modificada[id_nota, id_producto] for id_nota, id_producto in df_notas.index]) == 1
    
    # Resuelve
    print("status:", str(LpStatus[model.status]))
    model.solve()
    print("objetivo:", value(model.objective))
