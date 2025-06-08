import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports
import csv
import copy
import random
from mcts.motor_mcts import *
from mcts.motor_mcts_neuronal import mcts as mcts_red_neuronal
from mcts.agente_mcts import *

from utiles.fichas import *


def generar_csv_desde_mcts(ruta_csv, num_partidas, jugador=1, iteraciones=50):
    '''
    Esta es la función principal del agente. Devuelve un archivo .csv en el que cada fila representa un estado del tablero (64 números con el 
    valor de cada casilla) y una etiqueta basada en la última fila de la partida a la que pertenecen.

    PARÁMETROS
    - ruta_csv: Cadena que representa el archivo en el que serán almacenados los datos. Hay que tener en cuenta que este script se ejecuta desde
      la carpeta raíz del proyecto y no desde la carpeta mcts, en la que se encuentra este script.
    - num_partidas: Número de partidas a generar.
    - jugador: Jugador que va a ser entrenado
    - iteraciones: Entero que indicará al algoritmo MCTS cuántas iteraciones realizar.
    '''

    with open(ruta_csv, mode='w', newline='') as archivo:
        writer = csv.writer(archivo)

        # Para cada partida
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
            historial = [] # Historial de estados del tablero durante la partida

            while no_terminal(estado, turno):

                historial.append(copy.deepcopy(estado)) # Se añade el estado al historial de estados

                if turno == jugador: # En el turno del jugador a entrenar
                    accion = mcts_red_neuronal(estado, turno, iteraciones) # Escoger la acción basándose en el algoritmo MCTS
                    if accion is None: # Si no hay acción posible, se pasa turno
                        turno = 3 - turno
                        continue
                else: # En el turno del contrincante
                    acciones = movimientos_disponibles(estado, turno)
                    if acciones:
                        accion = random.choice(acciones) # Se realiza un movimiento aleatorio, en caso de tener acciones disponibles
                    else:
                        turno = 3 - turno # Si no se puede hacer nada, se pasa turno
                        continue

                estado[accion[0]][accion[1]] = turno # Se coloca la ficha en el lugar elegido

                # Se voltean las fichas y se pasa turno
                fichas_a_voltear = obtener_fichas_a_voltear(estado, accion[0], accion[1], turno)
                for (f, c) in fichas_a_voltear:
                    estado[f][c] = turno
                turno = 3 - turno

            historial.append(copy.deepcopy(estado)) # Se añade al historial el estado final de la partida
            recompensa = evaluar_final(estado, jugador) # Se evalua si el jugador a entrenar ha ganado o ha perdido

            # Se muestra en la consola para cada partida: la partida, el estado final del tablero (hay que tener en cuenta que la variable 
            # "estado" almacena, en este momento, el estado final de la partida), la cantidad de fichas de cada color y la etiqueta resultante.
            print(f"\n Partida {num + 1}:")
            print("Estado final del tablero:")
            for fila in estado:
                print(fila)
            blancos = sum(f.count(1) for f in estado)
            negros = sum(f.count(2) for f in estado)
            print(f"Fichas blancas (1): {blancos}")
            print(f"Fichas negras (2): {negros}")
            print(f"Etiqueta asignada (desde perspectiva del jugador {jugador}): {recompensa}")

            # Se escribe en el csv una fila por cada estado (tablero) almacenado, incluyendo las casillas del tablero 
            # y la etiqueta obtenida a partir del estado final.
            for tablero in historial:
                fila = tablero_a_fila(tablero, recompensa)
                writer.writerow(fila)


def main():

    ruta_salida = 'datos/datos_otelo_red_neuronal.csv'
    num_partidas = 20
    jugador = 1
    iteraciones = 20
    nombre_jugador = 'blanco' if jugador == 1 else 'negro'

    print(f"Generando {num_partidas} partidas para el jugador {nombre_jugador}...")
    generar_csv_desde_mcts(ruta_salida, num_partidas, jugador, iteraciones)
    print(f"CSV generado en '{ruta_salida}' con {num_partidas} partidas.")

if __name__ == '__main__':
    main()

