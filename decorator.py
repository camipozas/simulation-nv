import functools
import time

# Creamos un decorador que nos ayude a medir el tiempo de ejecución
# Sin tener que escribirlo para cada función
# código basado en https://realpython.com/primer-on-python-decorators/#timing-functions


def log(func):
    '''
    The @functools.wraps decorator uses the function functools.update_wrapper() to update special
    attributes 
    like __name__ and __doc__ that are used in the introspection

    :param func: the function to be decorated
    :return: A function wrapper.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Ejecutando función {func.__name__!r}")
        # ejecuta función con sus argumentos, y guarda valor retornado
        value = func(*args, **kwargs)
        # guarda tiempo de finalización
        print(f"Terminó función {func.__name__!r}")
        return value
    return wrapper

#  código basado en https://ellibrodepython.com/tiempo-ejecucion-python


def mide_tiempo(funcion):
    '''
    The mide_tiempo function takes a function as an argument and returns a function

    :param funcion: the function you want to decorate
    :return: The function that is being decorated.
    '''
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        duration = round(time.time() - inicio)
        print(duration)
        return c
    return funcion_medida
