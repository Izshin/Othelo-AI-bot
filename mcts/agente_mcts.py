import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
import csv
import copy
import random
from mcts.motor_mcts import *
from utiles.fichas import *


def tablero_a_fila(tablero, etiqueta):
    '''
    '''

    fila = []
    for fila_tablero in tablero:
        fila.extend(fila_tablero)
    fila.append(etiqueta)
    return fila

def evaluar_final(estado, jugador):
    '''
    '''

    ganador = obtener_ganador(estado)
    if ganador == jugador:
        return 1
    elif ganador == 0:
        return 0
    else:
        return -1

def generar_csv_desde_mcts(ruta_csv, num_partidas, jugador=1, iteraciones=100):
    '''
    '''

    with open(ruta_csv, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)

        for num in range(num_partidas):
            estado = [[0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,1,2,0,0,0],
                      [0,0,0,2,1,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0]]
            turno = 2  # negras empiezan
            historial = []

            while no_terminal(estado, turno):
                if turno == jugador:
                    accion = mcts(estado, turno, iteraciones)
                    if accion is None:
                        turno = 3 - turno
                        continue
                else:
                    acciones = movimientos_disponibles(estado, turno)
                    if acciones:
                        accion = random.choice(acciones)
                    else:
                        turno = 3 - turno
                        continue

                historial.append(copy.deepcopy(estado))
                fichas_a_voltear = obtener_fichas_a_voltear(estado, accion[0], accion[1], turno)
                estado[accion[0]][accion[1]] = turno
                for (f, c) in fichas_a_voltear:
                    estado[f][c] = turno
                turno = 3 - turno
            historial.append(copy.deepcopy(estado))

            recompensa = evaluar_final(estado, jugador)

            print(f"\n Partida {num + 1}:")
            print("Estado final del tablero:")
            for fila in estado:
                print(fila)
            blancos = sum(f.count(1) for f in estado)
            negros = sum(f.count(2) for f in estado)
            print(f"Fichas blancas (1): {blancos}")
            print(f"Fichas negras (2): {negros}")
            print(f"Etiqueta asignada (desde perspectiva del jugador {jugador}): {recompensa}")

            for tablero in historial:
                fila = tablero_a_fila(tablero, recompensa)
                writer.writerow(fila)


def main():

    ruta_salida = 'datos/datos_otelo.csv'
    num_partidas = 20
    jugador = 1
    iteraciones = 20
    nombre_jugador = 'blanco' if jugador == 1 else 'negro'

    print(f"Generando {num_partidas} partidas para el jugador {nombre_jugador}...")
    generar_csv_desde_mcts(ruta_salida, num_partidas, jugador, iteraciones)
    print(f"CSV generado en '{ruta_salida}' con {num_partidas} partidas.")

if __name__ == '__main__':
    main()

