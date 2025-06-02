# Imports
import pygame as pg

def obtener_fichas_a_voltear(tablero, fila, col, turno):
    '''
    Esta función devuelve una lista de coordenadas dentro del tablero en las que hay fichas
    que serán volteadas tras la colocación de una ficha en la posición dada como parámetro.

    PARÁMETROS
    - tablero: Matriz 8x8 con los valores que indican qué ficha hay en cada casilla.
    - fila: Fila de la posición en la que se va a colocar la ficha.
    - col: Columna de la posición en la que se va a colocar la ficha.
    - turno: Número que indica qué jugador está en su turno (0: ninguno, 1: blancas, 2: negras).
    '''

    # Lista con las coordenadas de las direcciones posibles. El primer número de cada tupla es la fila (1: 
    # una fila más, -1: una fila menos, 0: la misma fila). El segundo es la columna (1: una columna más...)
    direcciones = [(-1,-1),(-1, 0),(-1, 1),
                   ( 0,-1),        ( 0, 1),
                   ( 1,-1),( 1, 0),( 1, 1)]
    res = []
    
    # En este bucle se añaden, para cada una de las direcciones, las coordenadas de las fichas
    # que serán volteadas tras la colocación de una ficha en la posicion (fila, col).
    for df, dc in direcciones:
        nf = fila + df
        nc = col + dc
        fichas_por_voltear = [] # Lista de fichas que voltearán SÓLO en la dirección que vamos a recorrer.

        while 0 <= nf < 8 and 0 <= nc < 8:
            nueva_ficha = tablero[nf][nc]
            
            if nueva_ficha == 0:
                break # La casilla no tiene ninguna ficha, dejamos de recorrer la dirección.
            elif nueva_ficha == turno:
                if fichas_por_voltear:
                    res.extend(fichas_por_voltear) # Se añade al resultado de la función las fichas que voltearán.
                break # Como la casilla tiene una ficha del jugador que está en su turno, dejamos de recorrer la dirección.
            else:
                fichas_por_voltear.append((nf, nc))
            
            nf += df # Siguiente fila
            nc += dc # Siguiente columna

    return res

def movimientos_disponibles(tablero, turno):
    '''
    Esta función devuelve una lista con las coordenadas de los lugares en los que el jugador puede colocar una ficha.

    PARÁMETROS
    - tablero: Matriz 8x8 con los valores que indican qué ficha hay en cada casilla.
    - turno: Número que indica qué jugador está en su turno (0: ninguno, 1: blancas, 2: negras).
    '''

    res = []
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] == 0:
                fichas = obtener_fichas_a_voltear(tablero, fila, col, turno)
                if fichas:
                    res.append((fila,col))

    return res

def obtener_ganador(tablero):
    '''
    '''

    contador_negras = 0
    contador_blancas = 0
    for fila in range(8):
        for col in range(8):
            if tablero[fila][col] == 1:
                contador_blancas += 1
            if tablero[fila][col] == 2:
                contador_negras += 1
    
    if contador_negras > contador_blancas:
        return 2
    elif contador_blancas > contador_negras:
        return 1
    elif contador_blancas == contador_negras:
        return 0