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

# ---------------------------------------------------
# 1) Configuración inicial de Pygame
# ---------------------------------------------------
pg.init()
LONG_TABLERO = 640
LONG_CASILLA = 80
COLOR_FONDO = (0, 128, 0)
COLOR_LINEAS = (0, 0, 0)
pantalla = pg.display.set_mode((LONG_TABLERO, LONG_TABLERO))
pg.display.set_caption('Othello: Humano vs IA')
clock = pg.time.Clock()

# ---------------------------------------------------
# 2) Estado inicial del tablero
# ---------------------------------------------------
# 0: vacío, 1: blanca (IA), 2: negra (humano)
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

# Número de iteraciones para MCTS
ITER_MCTS = 80

# Bandera para saber si el humano movió en esta iteración
humano_movio = False

# ---------------------------------------------------
# 3) Bucle principal
# ---------------------------------------------------
run = True
while run:
    humano_movio = False  # Reseteamos al principio de cada frame

    # --- 3.1) Manejo de eventos de Pygame ---
    for evento in pg.event.get():
        # Si cierra la ventana
        if evento.type == pg.QUIT:
            run = False

        # Si el humano hace clic con el botón izquierdo y es su turno
        elif evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1 and turno == 2:
            if movimientos_disponibles(tablero, turno):
                x, y = evento.pos
                col = x // LONG_CASILLA
                fila = y // LONG_CASILLA

                # Verificamos que la casilla esté vacía y sea un movimiento válido
                if tablero[fila][col] == 0:
                    fichas_a_voltear = obtener_fichas_a_voltear(tablero, fila, col, turno)
                    if fichas_a_voltear:
                        # 3.1.1) Aplicar jugada del humano
                        tablero[fila][col] = turno
                        for (f, c) in fichas_a_voltear:
                            tablero[f][c] = turno

                        # Cambiamos el turno a la IA
                        turno = 1
                        humano_movio = True

    # --- 3.2) Si el humano movió, lo dibujamos YA y luego la IA piensa ---
    if humano_movio:
        # 3.2.1) Dibujar tablero con la jugada del humano YA reflejada
        dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
        pg.display.flip()

        # 3.2.2) Pequeño delay para que se vea la ficha del humano
        pg.time.delay(300)

        # 3.2.3) Turno de la IA (si tiene movimientos disponibles)
        if movimientos_disponibles(tablero, turno):
            movimiento_ia = mcts(tablero, turno, ITER_MCTS)

            if movimiento_ia is not None:
                fila_ia, col_ia = movimiento_ia
                fichas_ia = obtener_fichas_a_voltear(tablero, fila_ia, col_ia, turno)
                tablero[fila_ia][col_ia] = turno
                for (f, c) in fichas_ia:
                    tablero[f][c] = turno

                # 3.2.4) Dibujar tablero con la jugada de la IA
                dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
                pg.display.flip()

                # Otro pequeño delay para «ver» la jugada de la IA
                pg.time.delay(300)

        # 3.2.5) Tras la IA, vuelve el turno al humano (o se pasa si no hay movimientos)
        turno = 2
        if not movimientos_disponibles(tablero, turno):
            turno = 1

    # --- 3.3) Si no llegó un clic humano, puede que el humano no tenga jugadas ---
    else:
        # Si al inicio de la iteración no hay movimientos para el humano, pasamos turno a IA
        if turno == 2 and not movimientos_disponibles(tablero, turno):
            turno = 1

    # --- 3.4) Si es turno de IA y no acaba de mover el humano (ejemplo: pasó el humano) ---
    if turno == 1 and not humano_movio:
        if movimientos_disponibles(tablero, turno):
            # Dibujamos el estado ANTES de que la IA mueva (para claridad)
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

    # --- 3.5) Dibujar el tablero en cada iteración (por si no hubo clic humano) ---
    dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
    pg.display.flip()
    clock.tick(30)

# ---------------------------------------------------
# 4) Al cerrar, calculamos el resultado final
# ---------------------------------------------------
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
