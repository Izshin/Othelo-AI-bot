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
        '''
        Esta clase sirve para poder construir los nodos del árbol necesario para el uso del algoritmo de Monte Carlo Tree Search.

        ATRIBUTOS
        - estado: Estado del tablero que representa el nodo.
        - turno: Turno del jugador que puede colocar ficha.
        - padre: Nodo padre.
        - hijos: Lista de nodos hijo.
        - n: Número de veces que el nodo ha sido visitado por distintas partidas simuladas.
        - q: Recompensa total de todas las partidas simuladas que han visitado el nodo.
        - movimientos_por_hacer: Lista de movimientos posibles que representan los lugares en los que se puede colocar ficha.
        - movimiento: Movimiento que ha dado lugar a este nodo (concretamente, al tablero almacenado en el atributo "estado").
        '''
        self.estado = estado
        self.turno = turno
        self.padre = padre
        self.hijos = []
        self.n = 0
        self.q = 0
        self.movimientos_por_hacer = movimientos_disponibles(estado, turno)
        self.movimiento = movimiento


def mcts(tablero, turno, iteraciones=50):
    '''
    Esta función busca el mejor movimiento dado un tablero y un turno concreto, basándose en el algoritmo de Monte Carlo Tree Search.

    PARÁMETROS
    - tablero: Matriz 8x8 con los valores que indican qué ficha hay en cada casilla.
    - turno: Número que indica qué jugador está en su turno (0: ninguno, 1: blancas, 2: negras).
    - iteraciones: Número de iteraciones que realizará el algoritmo MCTS. 50 por defecto.
    '''

    # Primero crea un nodo raíz del árbol a partir del tablero dado como parámetro.
    root = Nodo(tablero, turno)
    # Comienza un bulce que se repetirá tantas veces como indique el número de iteraciones
    i = 0
    while i < iteraciones:
        # Elige el siguiente nodo del árbol, partiendo de su raíz.
        nodo = tree_policy(root)
        # Realiza una simulación de la partida desde el nodo anteriormente definido y calcula la recompensa según el resultado de la partida.
        recompensa = default_policy(nodo)
        # Retropropaga la recompensa por el nodo y por el raíz, incluyendo los nodos intermedios si los hubiere.
        backup(nodo, recompensa)
        i += 1
    
    # En caso de que el nodo raíz sea un nodo de estado terminal, se devuelve None.
    if not root.hijos:
        return None

    # En caso contrario, devolvemos el mejor movimiento a realizar partiendo de que el tablero se encuentre en el estado dado como parámetro.
    return mejor_movimiento(root)


def tree_policy(nodo):
    '''
    Esta función sirve para "bajar" un nivel en el árbol, partiendo de un nodo. Es decir, expande totalmente el nodo dado como parámetro, 
    elige el mejor hijo de todos y lo devuelve como resultado.

    PARÁMETROS
    - nodo: Nodo que queremos expandir totalmente y de entre cuyos hijos queremos elegir el mejor.
    '''

    # Empieza el bucle en el cual se comprueba que el nodo no sea nulo y que no sea un nodo con estado terminal.
    while nodo is not None and no_terminal(nodo.estado, nodo.turno):
        if nodo.movimientos_por_hacer:
            return expand(nodo) # Construimos uno de sus hijos si aún hay movimientos por hacer.
        elif nodo.hijos:
            nodo = mejor_hijo(nodo, 1.41) # Si ya no hay movimientos por hacer, el nodo ha sido expandido totalmente. Elegimos el mejor de los hijos.
        else:
            break # Si el nodo no tiene hijos terminamos el bucle.

    return nodo

def no_terminal(tablero, turno):
    '''
    Esta función comprueba que un tablero no se encuentre en estado terminal.

    PARÁMETROS
    - tablero: Matriz 8x8 con los valores que indican qué ficha hay en cada casilla.
    - turno: Número que indica qué jugador está en su turno (0: ninguno, 1: blancas, 2: negras).
    '''

    # Primero comprobamos que el jugador actual tiene movimientos disponibles.
    movimientos_propios = movimientos_disponibles(tablero, turno)
    # Después comprobamos que, al pasar turno, el oponente debe tener movimientos disponibles, pues puede ser que el jugador actual no los tenga pero el oponente sí.
    movimientos_oponente = movimientos_disponibles(tablero, 3 - turno) # "3 - turno" alterna el turno. Si turno es 2 (negras), 3-2=1 (blancas), si turno es 1, 3-1=2

    return movimientos_propios or movimientos_oponente

def expand(nodo):
    '''
    Esta función es crucial para construir el árbol, pues se encarga de construir los hijos de cada nodo. Aunque, en el contexto de la función y no de todo el
    algoritmo MCTS, crea y añade a la lista de hijos del nodo dado como parámetro uno de sus hijos.

    PARÁMETROS
    - nodo: Nodo que se va a expandir parcialmente. En este caso, esta función sólo va a construir uno de los hijos, para expandirlo totalmente (construir todos
      sus posibles hijos) será necesario llamar a esta función varias veces.
    '''

    # Eliminamos el último movimiento disponible de la lista de movimientos por hacer del nodo.
    movimiento = nodo.movimientos_por_hacer.pop()
    # Creamos un tablero nuevo para no modificar el tablero del propio nodo.
    nuevo_tablero = copy.deepcopy(nodo.estado)
    # Colocamos la ficha en la casilla indicada por el vector movimiento (fila, columna).
    nuevo_tablero[movimiento[0]][movimiento[1]] = nodo.turno
    # Volteamos las fichas que serán volteadas tras la colocación de la ficha.
    fichas_a_voltear = obtener_fichas_a_voltear(nuevo_tablero, movimiento[0], movimiento[1], nodo.turno)
    for (f, c) in fichas_a_voltear:
        nuevo_tablero[f][c] = nodo.turno
    # Creamos el hijo con: el nuevo tablero, el turno del otro jugador, el nodo padre y el movimiento que ha dado lugar a este nodo.
    hijo = Nodo(nuevo_tablero, 3 - nodo.turno, padre=nodo, movimiento=movimiento)
    # Añadimos el hijo a la lista de hijos del nodo padre.
    nodo.hijos.append(hijo)

    return hijo

def mejor_hijo(nodo, c=1.41):
    '''
    Esta función, dado un nodo y el parámetro c de la ecuación de UCT (pues nos basamos en UCT para elegir el mejor hijo), comprueba quién es el mejor 
    hijo. Haciendo un balance entre explotación y exploración, siendo lo último en función del parámetro c.

    PARÁMETROS
    - nodo: Nodo padre de entre cuyos hijos queremos elegir el mejor.
    - c: Constante de exploración. Cuanto más alta sea, más valoraremos explorar nodos desconocidos que explotar los nodos ya conocidos como "buenos".
      Toma el valor 1.41 por defecto.
    '''

    # En caso de que no haya nodos hijo porque se trate de un nodo de estado terminal, devolveremos el mismo nodo dado como parámetro.
    # Esto es sólo una comprobación para que la función no tenga un error al recorrer la lista de hijos y devuelva None, pero no es 
    # algo estrictamente necesario.
    if not nodo.hijos:
        return nodo

    # "elegido" será el mejor hijo hasta el momento
    elegido = None
    uct = None
    for h in nodo.hijos:
        if h.n == 0:
            uct_actual = float('inf') # Si, por lo que sea, h.n es 0, uct será infinito a causa de dividir por 0. Esto no es un paso estrictamente necesario.
        else:
            uct_actual = (h.q/h.n) + c*sqrt((2*log(nodo.n))/h.n)
        # Si el UCT más alto registrado todavía no es un número o si es más bajo que el recién calculado se le asigna ese UCT que acabamos de calcular
        if uct == None or uct_actual > uct:
            uct = uct_actual
            elegido = h

    return elegido

def default_policy(nodo):
    '''
    Esta función simula una partida desde el nodo dado como parámetro hasta el final. Una vez llegado al final de la partida devuelve la recompensa
    de dicho final. En caso de derrota (desde el punto de vista del jugador que tenía que colocar ficha en el primer movimiento de esta simulación)
    devuelve -1, en caso de empate 0 y en caso de victoria +1.

    PARÁMETROS
    - nodo: Nodo desde el cual se realiza la simulación de la partida hasta el final, eligiendo siempre acciones aleatorias en TODOS los turnos.
    '''

    # Primero copiamos el tablero inicial para no cambiar el tablero desde este nodo (aquí no recorremos el árbol, 
    # sólo simulamos la partida partiendo de ese nodo, pero no cambiamos de nodo en ningún momento, por eso no queremos
    # cambiar el estado del nodo dado como parámetro).
    nuevo_tablero = copy.deepcopy(nodo.estado)
    turno = nodo.turno
    jugador_inicial = turno

    # Empieza el bucle que terminará cuando el tablero se encuentre en un estado terminal
    while no_terminal(nuevo_tablero, turno):
        acciones = movimientos_disponibles(nuevo_tablero, turno)
        if acciones:
            movimiento = random.choice(acciones)
            nuevo_tablero[movimiento[0]][movimiento[1]] = turno # Colocar la ficha
            # Voltear las fichas que serán volteadas a causa de la colocación de la ficha anterior
            fichas_a_voltear = obtener_fichas_a_voltear(nuevo_tablero, movimiento[0], movimiento[1], turno)
            for (f, c) in fichas_a_voltear:
                nuevo_tablero[f][c] = turno
        # Cambiar de turno
        turno = 3 - turno

    # Aquí comprobamos quién ha ganado y devolvemos la recompensa correspondiente
    ganador = obtener_ganador(nuevo_tablero)
    if ganador == jugador_inicial:
        return 1
    elif ganador == 0:
        return 0
    else:
        return -1

def backup(nodo, recompensa):
    '''
    Esta función retropropaga la recompensa por todos los nodos hasta el nodo raíz del árbol.

    PARÁMETROS
    - nodo: Nodo final desde el cual retropagamos la recompensa.
    - recompensa: Etiqueta asignada en ese nodo final dado como parámetro y que será propagada por los nodos anteriores.
    '''

    while nodo is not None:
        nodo.n = nodo.n + 1 # Al nodo se le añade una visita, correspondiente a la partida simulada actualmente.
        nodo.q = nodo.q + recompensa # Al nodo se le añade la recompensa al total de recompensas de todas las partidas que han pasado por este nodo.
        nodo = nodo.padre # Retrocedemos en el árbol para propagar la recompensa por el nodo padre al nodo actual.

def mejor_movimiento(nodo):
    '''
    Esta función devuelve las coordenadas de la mejor posición en la que colocar una ficha en el turno actual.

    PARÁMETROS
    - nodo: Nodo desde el cuál se toma la decisión de hacer un movimiento u otro.
    '''

    mejor_hijo_nodo = mejor_hijo(nodo, 0)  # c=0 => solo explota, no explora, puesto que queremos el mejor movimiento asegurado
    return mejor_hijo_nodo.movimiento