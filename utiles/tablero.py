
# Imports
import pygame as pg

def dibujar_tablero(pantalla, tablero, long_casilla, color_fondo, color_lineas, color_blancas, color_negras):
    pantalla.fill(color_fondo)

    for fila in range(8):
        for col in range(8):
            x = col * long_casilla
            y = fila * long_casilla
            # Dibujar borde de la casilla
            pg.draw.rect(pantalla, color_lineas, (x, y, long_casilla, long_casilla), 1)

            valor = tablero[fila][col]
            if valor == 1:
                color = color_blancas
            elif valor == 2:
                color = color_negras
            else:
                continue  # casilla vacía, no se dibuja ficha

            centro = (x + long_casilla // 2, y + long_casilla // 2)
            radio = long_casilla // 2 - 5
            pg.draw.circle(pantalla, color, centro, radio)