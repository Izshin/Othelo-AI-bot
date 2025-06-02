fila_str = "1,2,1,2,1,0,1,2,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,2,1,2,1,2,1,2,1,0"

numeros = list(map(int, fila_str.split(',')))
tablero = numeros[:-1]  # Los primeros 64
etiqueta = numeros[-1]

print("Cantidad de 1:", tablero.count(1))
print("Cantidad de 2:", tablero.count(2))
print("Cantidad de 0:", tablero.count(0))
print("Etiqueta:", etiqueta)