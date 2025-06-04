import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras._tf_keras.keras.utils import set_random_seed
import pandas as pd
import numpy as np
from keras import Sequential, Input, Model
from keras._tf_keras.keras.layers import Dense
from keras._tf_keras.keras.layers import Normalization
from keras._tf_keras.keras.layers import Conv2D
from keras._tf_keras.keras.layers import Activation
from keras._tf_keras.keras.optimizers import SGD
from sklearn.preprocessing import label_binarize
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from keras._tf_keras.keras.datasets import mnist
from keras._tf_keras.keras.layers import Rescaling, Flatten
from keras._tf_keras.keras.utils import to_categorical
from keras._tf_keras.keras.metrics import Recall
from keras._tf_keras.keras.optimizers import Adam
import matplotlib.pyplot as plt
set_random_seed(394867)

# -------------------------------------------------------------------
# 1) DefinICIÓN EN Keras DE LA RED “value only”
# -------------------------------------------------------------------
#
# Arquitectura idéntica a OthelloNet, pero sin cabeza de política.
# Solo incluimos la cabeza de valor (tanh en [-1,1]).

input_layer = Input(shape=(8, 8, 2), name='estado_tablero')

# Bloque convolucional
x = Conv2D(64, (3, 3), padding='same', activation='relu', name='conv1')(input_layer)
x = Conv2D(128, (3, 3), padding='same', activation='relu', name='conv2')(x)
x = Conv2D(128, (3, 3), padding='same', activation='relu', name='conv3')(x)

# Aplanar y capa intermedia
x = Flatten(name='flatten')(x)
x = Dense(256, activation='relu', name='fc1')(x)

# Cabeza de valor: salida escalar en [-1,1]
value_output = Dense(1, activation='tanh', name='value_output')(x)

model_othello = Model(inputs=input_layer, outputs=value_output, name='OthelloNet_ValueOnly')

# Compilamos solo la cabeza de valor con MSE
model_othello.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss='mse',
    metrics=['mse']
)

model_othello.summary()


# -----------------------------------------------------------
# 2) CARGAR CSV Y EXTRAER X_raw, Y
# -----------------------------------------------------------
#
# Cada fila del CSV tiene 64 casillas (valores 0,1,2) y una etiqueta final en {+1,0,-1}.

df = pd.read_csv("datos/datos_otelo.csv", header=None)

# X_flat: forma (N, 64), valores {0,1,2}
X_flat = df.iloc[:, 0:64].values.astype(np.int32)

# Y: forma (N,), etiquetas float en {+1, 0, -1}
Y = df.iloc[:, 64].values.astype(np.float32)

# Convertir X_flat a X_raw con forma (N, 8, 8)
N = X_flat.shape[0]
X_raw = X_flat.reshape((N, 8, 8))


# -----------------------------------------------------------
# 3) FUNCIÓN PARA CONVERTIR (N,8,8) → (N,8,8,2) DOS CANALES
# -----------------------------------------------------------
def convertir_a_canales(X_raw):
    """
    Recibe X_raw de forma (N,8,8) con valores:
      0 = casilla vacía
      1 = ficha blanca
      2 = ficha negra
    Devuelve X_chan de forma (N,8,8,2) donde:
      canal 0 = 1.0 si había ficha negra (==2), 0 en otro caso
      canal 1 = 1.0 si había ficha blanca (==1), 0 en otro caso
    """
    N = X_raw.shape[0]
    X_chan = np.zeros((N, 8, 8, 2), dtype=np.float32)
    for i in range(N):
        for r in range(8):
            for c in range(8):
                if X_raw[i, r, c] == 2:
                    X_chan[i, r, c, 0] = 1.0
                elif X_raw[i, r, c] == 1:
                    X_chan[i, r, c, 1] = 1.0
    return X_chan

X = convertir_a_canales(X_raw)  # → (N, 8, 8, 2)


# -----------------------------------------------------------
# 4) ENTRENAR EL MODELO
# -----------------------------------------------------------
history = model_othello.fit(
    x=X,           # shape (N, 8, 8, 2)
    y=Y,           # shape (N,), etiquetas en {–1,0,+1}
    batch_size=64,
    epochs=30,
    validation_split=0.1,
    shuffle=True
)


model_othello.save("othello_neuronal_entrenada.h5")
