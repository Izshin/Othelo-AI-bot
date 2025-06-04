import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports de utilidades de Othello
from utiles.fichas import movimientos_disponibles, obtener_fichas_a_voltear, obtener_ganador
import copy
from math import sqrt, log
import random

# Imports para numpy y cargar el modelo
import numpy as np
from keras._tf_keras.keras.models import load_model


# -------------------------------------------------------------------
# 0) CARGAR EL MODELO DE VALOR ENTRENADO
# -------------------------------------------------------------------
# Usamos barras "/" para evitar escape inválido, y compile=False para
# evitar errores si el .h5 referenció a “mse” durante el guardado.
modelo_valor = load_model("red_neuronal/othello_neuronal_entrenada.h5", compile=False)


# -------------------------------------------------------------------
# 1) estado_a_tensor: convierte un tablero (8×8) a (1,8,8,2)
# -------------------------------------------------------------------
def estado_a_tensor(estado):
    """
    Convierte un tablero de Othello (matriz 8×8 de ints {0,1,2})
    en un numpy array de shape (1,8,8,2) con dos canales binarios:

      canal 0 = 1.0 si había ficha negra (==2)
      canal 1 = 1.0 si había ficha blanca (==1)

    Devolvemos un array dtype float32 listo para model.predict().
    """
    # “estado” puede ser lista de listas o np.array de shape (8,8)
    tablero = np.array(estado, dtype=np.int32)       # garantiza (8,8)

    tensor = np.zeros((1, 8, 8, 2), dtype=np.float32)
    tensor[0, :, :, 0] = (tablero == 2).astype(np.float32)
    tensor[0, :, :, 1] = (tablero == 1).astype(np.float32)
    return tensor


# -------------------------------------------------------------------
# 2) Nodo para el árbol de MCTS
# -------------------------------------------------------------------
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


# -------------------------------------------------------------------
# 3) Funciones auxiliares de MCTS (sin cambios)
# -------------------------------------------------------------------
def no_terminal(tablero, turno):
    movimientos_propios = movimientos_disponibles(tablero, turno)
    movimientos_oponente = movimientos_disponibles(tablero, 3 - turno)
    return bool(movimientos_propios) or bool(movimientos_oponente)


def expand(nodo):
    movimiento = nodo.movimientos_por_hacer.pop()
    nuevo_tablero = copy.deepcopy(nodo.estado)
    nuevo_tablero[movimiento[0]][movimiento[1]] = nodo.turno
    fichas = obtener_fichas_a_voltear(nuevo_tablero,
                                       movimiento[0],
                                       movimiento[1],
                                       nodo.turno)
    for (f, c) in fichas:
        nuevo_tablero[f][c] = nodo.turno
    hijo = Nodo(nuevo_tablero, 3 - nodo.turno, padre=nodo, movimiento=movimiento)
    nodo.hijos.append(hijo)
    return hijo


def mejor_hijo(nodo, c):
    if not nodo.hijos:
        return nodo

    elegido = None
    mejor_uct = -float('inf')
    for h in nodo.hijos:
        if h.n == 0:
            uct_actual = float('inf')
        else:
            uct_actual = (h.q / h.n) + c * sqrt((2 * log(nodo.n)) / h.n)
        if uct_actual > mejor_uct:
            mejor_uct = uct_actual
            elegido = h
    return elegido


def backup(nodo, recompensa):
    while nodo is not None:
        nodo.n += 1
        nodo.q += recompensa
        nodo = nodo.padre


def mejor_movimiento(nodo):
    return mejor_hijo(nodo, c=0.0).movimiento


# -------------------------------------------------------------------
# 4) default_policy con la red de valor (sin simulación aleatoria)
# -------------------------------------------------------------------
def default_policy(nodo):
    """
    En lugar de jugar aleatorio hasta el final, convertimos el estado
    nodo.estado (8×8) a tensor (1,8,8,2) y pedimos a la red un valor [-1,+1].
    """
    tensor = estado_a_tensor(nodo.estado)          # AHORA recibe (8,8) directamente
    v = modelo_valor.predict(tensor, verbose=0)    # salida shape (1,1)
    return float(v[0, 0])


# -------------------------------------------------------------------
# 5) tree_policy y mcts (idénticas a antes)
# -------------------------------------------------------------------
def tree_policy(nodo):
    while nodo is not None and no_terminal(nodo.estado, nodo.turno):
        if nodo.movimientos_por_hacer:
            return expand(nodo)
        elif nodo.hijos:
            nodo = mejor_hijo(nodo, c=1.4)
        else:
            break
    return nodo


def mcts(tablero, turno, iteraciones=500):
    root = Nodo(tablero, turno)
    for _ in range(iteraciones):
        nodo = tree_policy(root)
        recompensa = default_policy(nodo)
        backup(nodo, recompensa)

    if not root.hijos:
        return None
    return mejor_movimiento(root)


# -------------------------------------------------------------------
# 6) Ejemplo de uso en main
# -------------------------------------------------------------------
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
