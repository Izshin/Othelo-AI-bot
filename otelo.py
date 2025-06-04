# jugar_othello_con_ia.py

import sys
import os

# Para que encuentre 'mcts.motor_mcts_neuronal'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pygame as pg
import copy
from utiles.tablero import dibujar_tablero
from utiles.fichas import movimientos_disponibles, obtener_fichas_a_voltear, obtener_ganador

# Importamos la función mcts de nuestro motor neuronal
from mcts.motor_mcts_neuronal import mcts

#Configuramos pygame y el tablero
pg.init()
LONG_TABLERO = 640
LONG_CASILLA = 80
COLOR_FONDO = (0, 128, 0)
COLOR_LINEAS = (0, 0, 0)
pantalla = pg.display.set_mode((LONG_TABLERO, LONG_TABLERO))
pg.display.set_caption('Othello: Humano vs IA')
clock = pg.time.Clock()

#Establecemos el tablero inicial
tablero = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,2,0,0,0],
    [0,0,0,2,1,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]

# El humano (fichas negras=2) comienza
turno = 2

""" Número de iteraciones para MCTS, a menos iteraciones, más rápido pero menos preciso
 a más iteraciones, más preciso pero más lento."""
ITER_MCTS = 80

#Tenemos que saber si la persona ha movido para dejar un pequeño tiempo entre jugadas y que se vea la jugada
humano_movio = False

#Bucle principal del juego, se repetirá hasta que se cierre la ventana
run = True
while run:
    humano_movio = False  #Cada vez que el bucle comienza, tienes que mover porque el turno inicial es el tuyo, o te toca mover

  #Eventos de pygame
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            run = False

        # Si el humano hace clic con el botón izquierdo y es su turno
        elif evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1 and turno == 2:
            #Si ha hecho click, combrobamos que el movimiento es valido
            if movimientos_disponibles(tablero, turno):
                x, y = evento.pos
                col = x // LONG_CASILLA
                fila = y // LONG_CASILLA

                # Verificamos que la casilla esté vacía
                if tablero[fila][col] == 0:
                    fichas_a_voltear = obtener_fichas_a_voltear(tablero, fila, col, turno)
                    if fichas_a_voltear:
                        #Se voltean las fichas, si procede
                        tablero[fila][col] = turno
                        for (f, c) in fichas_a_voltear:
                            tablero[f][c] = turno

                        #Le damos a la IA el movimiento
                        turno = 1
                        humano_movio = True

    #Si la persona acaba de hacer un movimiento, dibujamos el tablero y esperamos un poco para que la IA empiece a pensar
    if humano_movio:
        #Dibujamos tablero
        dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
        pg.display.flip()

        #Pequeña espera
        pg.time.delay(300)

        #Turno de la IA
        if movimientos_disponibles(tablero, turno):
            #Realiza las iteraciones de MCTS y la IA piensa su movimiento
            movimiento_ia = mcts(tablero, turno, ITER_MCTS)

            #Si la IA tiene un movimiento valido, lo realiza
            if movimiento_ia is not None:
                fila_ia, col_ia = movimiento_ia
                fichas_ia = obtener_fichas_a_voltear(tablero, fila_ia, col_ia, turno)
                tablero[fila_ia][col_ia] = turno
                for (f, c) in fichas_ia:
                    tablero[f][c] = turno

                #Se dibuja el tablero para reflejar el movimiento de la IA
                dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
                pg.display.flip()

                #Pequeña espera para que se vea el movimiento de la IA
                pg.time.delay(300)

        #Se vuelve al turno de la persona
        turno = 2
        if not movimientos_disponibles(tablero, turno):
            turno = 1

    else:
        #Si no hay movimiento disponible para la persona, se pasa el turno a la IA
        if turno == 2 and not movimientos_disponibles(tablero, turno):
            turno = 1

    #Si es turno de IA y la persona no ha movido, la IA piensa y hace su movimiento
    if turno == 1 and not humano_movio:
        if movimientos_disponibles(tablero, turno):
            #Dibujamos el tablero antes del movimiento de la IA, con una espera para que se vea el movimiento
            dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
            pg.display.flip()
            pg.time.delay(300)

            movimiento_ia = mcts(tablero, turno, ITER_MCTS)
            if movimiento_ia is not None:
                fila_ia, col_ia = movimiento_ia
                fichas_ia = obtener_fichas_a_voltear(tablero, fila_ia, col_ia, turno)
                tablero[fila_ia][col_ia] = turno
                for (f, c) in fichas_ia:
                    tablero[f][c] = turno

            # Dibujamos tras la IA mover
            dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
            pg.display.flip()
            pg.time.delay(300)

        # Devolvemos turno al humano a menos que éste no pueda mover
        turno = 2
        if not movimientos_disponibles(tablero, turno):
            turno = 1

    """Dibujamos el tablero en cada iteración del bucle, no hace falta que se dibuje puesto que en el resto del bucle se dibuja, 
    pero por si acaso para que se vea el tablero actualizado"""
    dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
    pg.display.flip()
    clock.tick(30)

#Cerramos pygame y mostramos el resultado final
pg.quit()

blancas = sum(fila.count(1) for fila in tablero)
negras   = sum(fila.count(2) for fila in tablero)
print("Partida finalizada.")
print(f"Fichas blancas (IA): {blancas}")
print(f"Fichas negras (Humano): {negras}")
if blancas > negras:
    print("¡La IA (blancas) ha ganado!")
elif negras > blancas:
    print("¡Tú (negras) has ganado!")
else:
    print("¡Empate!")
