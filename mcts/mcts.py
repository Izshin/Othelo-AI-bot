# Imports
from utiles.fichas import *
import copy
from math import sqrt, log
import random

class Nodo:
    def __init__(self, estado, turno, padre=None):
        self.estado = estado
        self.turno = turno
        self.padre = padre
        self.hijos = []
        self.n = 0
        self.q = 0
        self.movimientos_por_hacer = movimientos_disponibles(estado, turno)
        self.movimiento = None


def mcts(tablero, turno, iteraciones=500):
    '''
    '''

    root = Nodo(tablero, turno)
    i = 0
    while i <= iteraciones:
        nodo = tree_policy(root)
        recompensa = default_policy(nodo)
        backup(nodo, recompensa)
        i += 1

    return mejor_movimiento(root)


def tree_policy(nodo):
    '''
    '''

    while no_terminal(nodo.estado, nodo.turno):
        if nodo.movimientos_por_hacer:
            return expand(nodo)
        else:
            nodo = mejor_hijo(nodo, 1.4)

    return nodo

def no_terminal(tablero, turno):
    '''
    '''

    movimientos_propios = movimientos_disponibles(tablero, turno)
    # "3 - turno" alterna el turno. Si turno es 2 (negras), 3-2=1 (blancas), si turno es 1, 3-1=2
    movimientos_oponente = movimientos_disponibles(tablero, 3 - turno)

    return not movimientos_propios and not movimientos_oponente

def expand(nodo):
    '''
    '''

    movimiento = nodo.movimientos_por_hacer.pop()
    nuevo_tablero = copy.deepcopy(nodo.tablero)
    nuevo_tablero[movimiento[0]][movimiento[1]] = nodo.turno
    hijo = Nodo(nuevo_tablero, 3 - nodo.turno, padre=nodo)
    nodo.hijos.append(hijo)

    return hijo

def mejor_hijo(nodo, c):

    elegido = None
    uct = None
    for h in nodo.hijos:
        uct_actual = (h.q/h.n) + c*sqrt((2*log(nodo.n))/h.n)
        if uct == None or uct_actual > uct:
            uct = uct_actual
            elegido = h

    return elegido

# funciones en proceso
def default_policy(nodo):
    '''
    '''

    while no_terminal(nodo.estado, nodo.turno):
        acciones = movimientos_disponibles(nodo.estado, nodo.turno)
        if acciones:
            movimiento = random.choice(acciones)
            nuevo_tablero = copy.deepcopy(nodo.tablero)
            nuevo_tablero[movimiento[0]][movimiento[1]] = nodo.turno
        else:
            nuevo_tablero = copy.deepcopy(nodo.tablero)
        

    return nodo

def backup(nodo):
    return None

def mejor_movimiento(tablero, c):
    return tablero