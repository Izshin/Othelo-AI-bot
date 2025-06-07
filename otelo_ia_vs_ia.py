# jugar_othello_ai_vs_ai.py

import sys
import os

# Para que Python encuentre los paquetes 'mcts' y 'utiles'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pygame as pg
from utiles.tablero import dibujar_tablero
from utiles.fichas import movimientos_disponibles, obtener_fichas_a_voltear, obtener_ganador

# Importamos ambos motores MCTS
from mcts.motor_mcts_neuronal import mcts as mcts_neuronal
from mcts.motor_mcts           import mcts as mcts_classic

# ---------------------------------------------------
# 1) Configuración de Pygame y constantes
# ---------------------------------------------------
pg.init()
LONG_TABLERO  = 640
LONG_CASILLA  = 80
COLOR_FONDO   = (0, 128, 0)
COLOR_LINEAS  = (0, 0, 0)
pantalla      = pg.display.set_mode((LONG_TABLERO, LONG_TABLERO))
pg.display.set_caption('Othello: IA Neuronal vs IA Clásica')
clock         = pg.time.Clock()

# ---------------------------------------------------
# 2) Tablero inicial
# ---------------------------------------------------
# 0 = vacío, 1 = blancas (MCTS clásico), 2 = negras (MCTS+neuronal)
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

turno = 2  #Empiezan las negras

# ---------------------------------------------------
# 3) Parámetros de búsqueda
# ---------------------------------------------------
ITER_CLASSIC  = 80  # iteraciones para MCTS puro
ITER_NEURONAL =  80  # iteraciones para MCTS+red

#Mismma cantidad de iteraciones para ambas IAs, para que la partida sea justa

# ---------------------------------------------------
# 4) Bucle principal
# ---------------------------------------------------
run = True
while run:
    # Aseguramos que la cola de eventos está en un estado válido
    pg.event.pump()

    # Intentamos recoger los eventos, protegiéndonos de posibles errores
    try:
        events = pg.event.get()
    except SystemError:
        pg.event.pump()
        events = pg.event.get()

    # Procesamos únicamente cierre de ventana
    for event in events:
        if event.type == pg.QUIT:
            run = False

    # Si ambas IAs no tienen movimientos posibles, terminamos
    if not movimientos_disponibles(tablero, 1) and not movimientos_disponibles(tablero, 2):
        break

    # Dibujamos el tablero actual
    dibujar_tablero(pantalla, tablero, LONG_CASILLA, COLOR_FONDO, COLOR_LINEAS)
    pg.display.flip()
    pg.time.delay(300)

    # Turno de MCTS clásico (blancas)
    if turno == 1 and movimientos_disponibles(tablero, 1):
        mov = mcts_classic(tablero, 1, ITER_CLASSIC)

    # Turno de MCTS+neuronal (negras)
    elif turno == 2 and movimientos_disponibles(tablero, 2):
        mov = mcts_neuronal(tablero, 2, ITER_NEURONAL)

    else:
        # Si el jugador de turno no puede mover, cambiamos turno y seguimos
        turno = 3 - turno
        continue

    # Aplicamos el movimiento si existe
    if mov is not None:
        f, c = mov
        fichas = obtener_fichas_a_voltear(tablero, f, c, turno)
        tablero[f][c] = turno
        for (fr, cc) in fichas:
            tablero[fr][cc] = turno

    # Cambiamos de turno
    turno = 3 - turno

    # Controlamos FPS para visualización adecuada
    clock.tick(0)

# Quit Pygame al salir del bucle
pg.quit()

# ---------------------------------------------------
# 5) Mostrar resultado final
# ---------------------------------------------------
blancas = sum(row.count(1) for row in tablero)
negras  = sum(row.count(2) for row in tablero)
print("Partida finalizada.")
print(f"Fichas blancas (MCTS clásico): {blancas}")
print(f"Fichas negras (MCTS+neuronal): {negras}")
if blancas > negras:
    print("¡MCTS clásico gana!")
elif negras > blancas:
    print("¡MCTS+neuronal gana!")
else:
    print("¡Empate!")
