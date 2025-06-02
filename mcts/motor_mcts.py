import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
from utiles.fichas import *
import copy
from math import sqrt, log
import random

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


def mcts(tablero, turno, iteraciones=500):
    '''
    '''

    root = Nodo(tablero, turno)
    i = 0
    while i < iteraciones:
        nodo = tree_policy(root)
        recompensa = default_policy(nodo)
        backup(nodo, recompensa)
        i += 1

    return mejor_movimiento(root)


def tree_policy(nodo):
    '''
    '''

    while nodo is not None and no_terminal(nodo.estado, nodo.turno):
        if nodo.movimientos_por_hacer:
            return expand(nodo)
        elif nodo.hijos:
            nodo = mejor_hijo(nodo, 1.4)
        else:
            break

    return nodo

def no_terminal(tablero, turno):
    '''
    '''

    movimientos_propios = movimientos_disponibles(tablero, turno)
    # "3 - turno" alterna el turno. Si turno es 2 (negras), 3-2=1 (blancas), si turno es 1, 3-1=2
    movimientos_oponente = movimientos_disponibles(tablero, 3 - turno)

    return movimientos_propios or movimientos_oponente

def expand(nodo):
    '''
    '''

    movimiento = nodo.movimientos_por_hacer.pop()
    nuevo_tablero = copy.deepcopy(nodo.estado)
    nuevo_tablero[movimiento[0]][movimiento[1]] = nodo.turno
    fichas_a_voltear = obtener_fichas_a_voltear(nuevo_tablero, movimiento[0], movimiento[1], nodo.turno)
    for (f, c) in fichas_a_voltear:
        nuevo_tablero[f][c] = nodo.turno
    hijo = Nodo(nuevo_tablero, 3 - nodo.turno, padre=nodo, movimiento=movimiento)
    nodo.hijos.append(hijo)

    return hijo

def mejor_hijo(nodo, c):
    '''
    '''

    if not nodo.hijos:
        return nodo

    elegido = None
    uct = None
    for h in nodo.hijos:
        if h.n == 0:
            uct_actual = float('inf')
        else:
            uct_actual = (h.q/h.n) + c*sqrt((2*log(nodo.n))/h.n)
        if uct == None or uct_actual > uct:
            uct = uct_actual
            elegido = h

    return elegido

def default_policy(nodo):
    '''
    '''

    nuevo_tablero = copy.deepcopy(nodo.estado)
    turno = nodo.turno
    jugador_inicial = turno

    while no_terminal(nuevo_tablero, turno):
        acciones = movimientos_disponibles(nuevo_tablero, turno)
        if acciones:
            movimiento = random.choice(acciones)
            nuevo_tablero[movimiento[0]][movimiento[1]] = turno
        turno = 3 - turno

    ganador = obtener_ganador(nuevo_tablero)
    if ganador == jugador_inicial:
        return 1
    elif ganador == 0:
        return 0
    else:
        return -1

def backup(nodo, recompensa):
    '''
    '''

    while nodo is not None:
        nodo.n = nodo.n + 1
        nodo.q = nodo.q + recompensa
        nodo = nodo.padre

def mejor_movimiento(nodo):
    '''
    '''

    mejor_hijo_nodo = mejor_hijo(nodo, 0)  # c=0 => solo explota, no explora
    return mejor_hijo_nodo.movimiento