
# Imports
import pygame as pg

def dibujar_tablero(pantalla, tablero, long_casilla, color_fondo, color_lineas):
    '''
    Esta función sirve para dibujar el tablero resultante de cada movimiento de los dos jugadores.
    
    PARÁMETROS
    - pantalla: Pantalla de pygame necesaria para que la función aplique los cambios.
    - tablero: Matriz 8x8 con los valores que indican qué fichas hay en cada casilla.
    - long_casilla: Longitud, en píxeles, del lado de cada casilla.
    - color_fondo: Color del fondo del tablero.
    - color_lineas: Color de las líneas que separan las casillas.
    '''

    # Dibujar fondo del tablero
    pantalla.fill(color_fondo)
    # Localización de cada casilla
    for fila in range(8):
        for col in range(8):
            x = col * long_casilla
            y = fila * long_casilla
            # Dibujar bordes de la casilla: (x,y) son las coordenadas del píxel superior izquierdo de toda la casilla
            pg.draw.rect(pantalla, color_lineas, (x, y, long_casilla, long_casilla), 1)

            valor = tablero[fila][col]
            if valor == 1:
                color = (255, 255, 255) # blanca
            elif valor == 2:
                color = (0, 0, 0) # negra
            else:
                continue  # sin ficha

            centro = (x + long_casilla // 2, y + long_casilla // 2)
            radio = long_casilla // 2 - 5
            # Dibujar ficha
            pg.draw.circle(pantalla, color, centro, radio)