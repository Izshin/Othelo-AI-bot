# Imports
import pygame as pg

def obtener_fichas_a_voltear(tablero, fila, col, turno):
    '''
    '''
    direcciones = [(-1,-1),(-1, 0),(-1, 1),
                   ( 0,-1)        ,( 0, 1),
                   ( 1,-1),( 1, 0),( 1, 1)]
    res = []

    for df, dc in direcciones:
        nf = fila + df
        nc = col + dc
        fichas_por_voltear = []

        while 0 <= nf < 8 and 0 <= nc < 8:
            nueva_ficha = tablero[nf][nc]
            
            if nueva_ficha == 0:
                break
            elif nueva_ficha == turno:
                if fichas_por_voltear:
                    res.extend(fichas_por_voltear)
                break
            else:
                fichas_por_voltear.append((nf, nc))
            
            nf += df
            nc += dc

    return res