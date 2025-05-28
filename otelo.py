# Imports
import pygame as pg
from utiles.tablero import *
from utiles.fichas import *

# Setup de pygame
pg.init()

# Constantes
LONG_TABLERO = 640
LONG_CASILLA = 80
COLOR_FONDO = (0, 128, 0)
COLOR_LINEAS = (0, 0, 0)

# Creacion de la ventana y booleano de ejecución
pantalla = pg.display.set_mode((LONG_TABLERO, LONG_TABLERO))
pg.display.set_caption('Otelo')
run = True

# Creación del tablero junto con las fichas iniciales (0: sin ficha, 1: blanca, 2: negra)
tablero = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,1,2,0,0,0],
           [0,0,0,2,1,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]

# Turno inicial - empieza el jugador (que controlará las fichas negras)
turno = 2

while run:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            run = False

        elif evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1:
            x, y = evento.pos
            col = x // LONG_CASILLA
            fila = y // LONG_CASILLA
            fichas_a_voltear = obtener_fichas_a_voltear(tablero, fila, col, turno)

            if tablero[fila][col] == 0 and fichas_a_voltear:
                tablero[fila][col] = turno
                for f,c in fichas_a_voltear:
                    tablero[f][c] = turno
                turno = 1 if turno == 2 else 2

    dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
    pg.display.flip()

pg.quit()

