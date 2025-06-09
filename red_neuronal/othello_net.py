import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras._tf_keras.keras.utils import set_random_seed
import pandas as pd
import numpy as np
from keras import Input, Model
from keras._tf_keras.keras.layers import Dense
from keras._tf_keras.keras.layers import Conv2D
from keras._tf_keras.keras.layers import Flatten
from keras._tf_keras.keras.optimizers import Adam
import matplotlib.pyplot as plt
from keras._tf_keras.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras._tf_keras.keras.optimizers.schedules import CosineDecayRestarts
from keras._tf_keras.keras.layers import BatchNormalization, Activation, Dropout

set_random_seed(394867)

#Definimos la red para othello, tenemos una entrada de 8x8 con 2 canales (fichas negras y blancas).

capa_entrada = Input(shape=(8, 8, 2), name='estado_tablero')

"""Por otra parte la red tiene 3 capas ocultas con 64, 128 y 128 filtros respectivamente, todas con activación ReLU.
Esta funciona mediante convoluciones 3x3 que significa que cada creamos "plantillas" (llamadas filtros) que ocupan 3 filas y 3 
columnas que recorren el tablero de entrada tratando de detectar ciertos patrones en este mismo tablero.

Matematicamente, estas plantillas o filtros 3x3 tienen pesos asociados a cada una de sus posiciones, y al moverse por la imagen de entrada,
realizan una operación de convolución, que significa que multiplican cada valor de la casilla del filtro por el valor de la casilla del 
tablero con la que se superponga y luego suman todos esos productos para obtener un único valor de salida.

El centro de los filtro corresponden a una poscion del tablero 8x8, y el valor de salida se coloca en la posicion correspondiente
de ese centro, en una nueva matriz 8x8 que, tras aplicar todo el movimiento del filtro, se convierte en la nueva entrada de la capa 
de salida."""



"""Estas capas de convolución se aplican unas encima de otras para detectar patrones cada vez más complejos o abstractos.

La primera capa detecta patrones simples, como líneas de fichas blancas o negras huecos vacios o huecos donde hay fichas.

La segunda capa detecta combinaciones de estos patrones, como dos fichas blancas rodeando a una ficha negra,
o una ficha negra en la diagonal del tablero, justo antes de una esquina, lo que indica una posible jugada a futuro.

La tercera capa, vuelve a juntar estos patrones, detectando jugadas mas a futoro o estrategicas, como una jugada que en 4
turnos pueda llevar a bloquear al oponente

Tras esto, se aplanan los datos de la ultima capa convolucional a un vector de 256 elementos que se pasa a la siguiente capa de la red,
 estos valores forman una imagen global del estado del tablero, de lo buena o mala que es la posción

Finalmente, se transforman estos 256 valores en un unico valor mediante activacion tanh que nos coloca el valor entre -1 y 1
a menor el valor, peor la posicion, a mayor el valor, lo contrario, mejor la posicion."""




x = Conv2D(64, (3, 3), padding='same', activation="relu", name='conv1')(capa_entrada)


x = Conv2D(128, (3, 3), padding='same', activation="relu", name='conv2')(x)


x = Conv2D(128, (3, 3), padding='same', activation="relu", name='conv3')(x)


x = Flatten(name='flatten')(x)

"""Añadimos una capa de Dropout, que se encarga de regular el ajuste de la red neuronal en cada epoca, para ello, se "apagan"
 aleatoriamente ciertas neuronas,haciendo que estas no den valores y por ende, 
 no se tengan en cuenta para el ajuste de los pesos de la red."""

x = Dropout(0.5, name='dropout_fc')(x)

x = Dense(256, activation='relu', name='fc1')(x)

prob_victoria = Dense(1, activation='tanh', name='prob_victoria')(x)

model_othello = Model(inputs=capa_entrada, outputs=prob_victoria, name='Othello_Net')

"""Compilamos con optimizador Adam, ampliamente usado en redes neuronales, y como error la media cuadrática (MSE) ya que queremos
minimizar la diferencia entre el valor predicho y el valor real de la etiqueta, que es tambien un valor entre -1 y 1."""

opt = Adam(learning_rate=1e-4)
model_othello.compile(
    optimizer=opt,
    loss='mse',
    metrics=['mse']
)

"""Con summary mostramos la red neuronal"""
model_othello.summary()



"""Leemos el csv con los datos de entrenamiento generados por el agente MCTS"""
df = pd.read_csv("datos/datos_otelo_red_neuronal.csv", header=None)

"""Establecemos que los primeros 64 valores de cada fila son casillas y lo pasamos a numpy para que sea más rápido de procesar."""
X_plano = df.iloc[:, 0:64].values.astype(np.int32)

"""Lo mismo para las etiquetas, excepto que estas son el ultimo valor de cada fila"""
Y = df.iloc[:, 64].values.astype(np.float32)

"""Es necesario establecer N porque asi numpy puede convertir los vectores planos de 64 valores en matrices de 8x8,
si no se define N, numpy no sabe cuando parar de leer los valores"""
N = X_plano.shape[0]
x_tablero = X_plano.reshape((N, 8, 8))


"""Tenemos que convertir los valores de las casillas del tablero 0,1,2 a canales de tipo [0/1, 0/1] para poder entrenar la red neuronal.

Esto se hace asi pues al tener las casillas por canales en lugar de valores de 0,1 o 2, hace que la red neuronal no se confunda,
si tuvieramos valores de 0,1 o 2, la red neuronal tendria que "adivinar" que los valores 0,1,2 son fichas negras, blancas o vacias, 
y que, por ejemplo, 2 no vale mas que 1, sino que es una ficha negra."""

"""Para ello tomamos el numero de filas N del tablero cocnreto y creamos una matriz de ceros de tamaño (N, 8, 8, 2).
    Luego recorremos cada casiila de cada fila en el tablero 8x8, lo transofrmamos al canal y sustituimos el 0 que haya en esa posicion
    por el valor transformado a canal.

    Con el valor N de x_can, establecemos el numero de tableros 8x8 que tenemos en total."""

def convertir_a_canales(x_tablero): 
    N = x_tablero.shape[0]
    X_can = np.zeros((N, 8, 8, 2), dtype=np.float32)
    for i in range(N):
        for r in range(8):
            for c in range(8):
                if x_tablero[i, r, c] == 2:
                    X_can[i, r, c, 0] = 1.0
                elif x_tablero[i, r, c] == 1:
                    X_can[i, r, c, 1] = 1.0
    
    return X_can

    
    
  
X = convertir_a_canales(x_tablero)


"""Como en el conjunto de entrenammiento hay muchas mas victorias que derrotas o empates, establecemos un
peso a cada etiqueta para que se balancee el entrenamiento y no tenga un sesgo hacia las victorias."""

frecuencia_pesos = df[64].value_counts(normalize=True).to_dict() 
pesos_etiquetas = {
    -1: 1.0 / frecuencia_pesos[-1],
     0: 1.0 / frecuencia_pesos[0],
     1: 1.0 / frecuencia_pesos[1],
}


"""Con el objetivo de ahorrar tiempo, colocamos una parada temprana, que para el entrenamiento si no mejora durante 10 epochs"""
parada = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

"""Para precisar al llegar a un minimo local bueno, realizamos una reduccion de la tasa de aprendizaje
si no mejor la validacion durante 5 epocas, reduciendo la tasa a un 80% de la actual, hasta un minimo de 1e-6."""
reducir_ap = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.8,
    patience=5,
    min_lr=1e-6,
    verbose=1
)

"""Con los datos ya preparados, en canales y con las etiquetas, entrenamos la red, usando un batch de 128 y hasta 30 epochs,
con un 10% para validación, shuffle, balanceo de clases y callbacks."""
entrenado = model_othello.fit(
    x=X,
    y=Y,
    batch_size=128,
    epochs=30,
    validation_split=0.1,
    shuffle=True,
    callbacks=[parada, reducir_ap],
    class_weight=pesos_etiquetas
)

"""Por último, guardamos la red entrenada en .h5 para cargarla en el motor MCTS que integra la red."""
model_othello.save("red_neuronal/othello_neuronal_entrenada.h5")
