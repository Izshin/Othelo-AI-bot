import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utiles.fichas import movimientos_disponibles, obtener_fichas_a_voltear, obtener_ganador
import numpy as np
from keras._tf_keras.keras.models import load_model

from mcts.motor_mcts import *


"""Cargamos el modelo anteriormente creado, entrenado y guardado en othello_net"""
modelo_valor = load_model("red_neuronal/othello_neuronal_entrenada.h5", compile=False)


def estado_a_tensor(estado): #Como entrada tiene un tablero 8x8 con valores 0, 1 o 2.
    """
    Puesto que en este caso solo pasaremos un tablero, en lugar de un conjunto de datos con varios tableros,
    convertimos el tablero 8x8 directamente a un tensor de forma (1, 8, 8, 2).

    Relizamos una oprecion muy similar a "convertir_a_canales" de la red neuronal. Pero con un tablero nada mas

    Para ello, creamos el tensor (o tablero de salida) de ceros y de la misma forma, recorremos el tablero de entrada 8x8, y sustiuimos
    los valores transformados a canal en el tensor (o tablero de salida) de ceros.
    """

    tablero = np.array(estado, dtype=np.int32)       

    tensor = np.zeros((1, 8, 8, 2), dtype=np.float32)
    tensor[0, :, :, 0] = (tablero == 2).astype(np.float32)
    tensor[0, :, :, 1] = (tablero == 1).astype(np.float32)
    return tensor #Como salida tiene un tensor (similar a un tablero) por canales en lugar de valores



class Nodo:
    def __init__(self, estado, turno, padre=None, movimiento=None):
        self.estado = estado
        self.turno = turno
        self.padre = padre
        self.hijos = []
        self.n = 0
        self.q = 0
        self.movimientos_por_hacer = movimientos_disponibles(estado, turno)
        self.movimiento = movimiento


def default_policy(nodo): #Como entrada tiene el nodo inicial, del que solo tomaremos el estado que es el tablero 8x8.
    """
    En lugar de jugar aleatorio hasta el final, convertimos el estado
    nodo.estado (8×8) a tensor (1,8,8,2) y pedimos a la red un valor [-1,+1].

    Con predict, le pasamos a la red el tablero convertido a tensor y nos da el valor de la recompensa,
    colocamos verbose=0 para que no muestre la progresion de la predicción.

    Como la red neuronal devuelve una matriz de 1x1, tenemos que acceder a ese valor con el índice v[0, 0], y tomarlo como float
    """
    
    tensor = estado_a_tensor(nodo.estado)          
    v = modelo_valor.predict(tensor, verbose=0)    
    return float(v[0, 0]) #Y como salida tiene el valor de recompensa predicho por la red

def mcts(tablero, turno, iteraciones=500):
    root = Nodo(tablero, turno)
    for _ in range(iteraciones):
        nodo = tree_policy(root)
        recompensa = default_policy(nodo)
        backup(nodo, recompensa)

    if not root.hijos:
        return None
    return mejor_movimiento(root)




#Un ejemplo de uso
if __name__ == "__main__":
    estado_inicial = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    turno_inicial = 1   # blancas empieza
    iteraciones = 100

    movimiento = mcts(estado_inicial, turno_inicial, iteraciones)
    print("Movimiento elegido por MCTS + red de valor:", movimiento)
