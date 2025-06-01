import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras._tf_keras.keras.utils import set_random_seed
import pandas as pd
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
# Definición en Keras de la red OthelloNet (igual que en PyTorch)
# -------------------------------------------------------------------

# 1) Capa de entrada: un tablero 8×8 con dos canales
#    • Canal 0 = piezas negras  (valor 1 cuando haya ficha negra)
#    • Canal 1 = piezas blancas (valor 1 cuando haya ficha blanca)
#    Input(shape=(8, 8, 2))
input_layer = Input(shape=(8, 8, 2), name='estado_tablero')

# 2) Bloque convolucional idéntico a PyTorch:
#    Conv2D(64, 3×3, padding='same') → ReLU
#    Conv2D(128, 3×3, padding='same') → ReLU
#    Conv2D(128, 3×3, padding='same') → ReLU
x = Conv2D(64, (3, 3), padding='same', activation='relu', name='conv1')(input_layer)
x = Conv2D(128, (3, 3), padding='same', activation='relu', name='conv2')(x)
x = Conv2D(128, (3, 3), padding='same', activation='relu', name='conv3')(x)

# 3) Aplanamos (Flatten) y una capa densa intermedia de 256 neuronas + ReLU
x = Flatten(name='flatten')(x)
x = Dense(256, activation='relu', name='fc1')(x)

# 4) Cabeza de política (policy head)
#    - Raw logits de tamaño 64 (una por cada posible casilla 8×8 = 64)
#    - Softmax para convertir en probabilidad sobre cada acción
policy_logits = Dense(64, name='policy_logits')(x)
policy_output = Activation('softmax', name='policy_output')(policy_logits)

# 5) Cabeza de valor (value head)
#    - Salida escalar única en [-1,1] mediante tanh
value_output = Dense(1, activation='tanh', name='value_output')(x)

# 6) Construcción del modelo con dos salidas
model_othello = Model(
    inputs=input_layer,
    outputs=[policy_output, value_output],
    name='OthelloNet_Keras'
)

# 7) Compilamos:
#    • Para ‘policy_output’: categorical_crossentropy (si tienes etiquetas de política)
#    • Para ‘value_output’: mean squared error (MSE), pues aquí queremos aproximar el valor real ∈ [–1,1]
model_othello.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss={
        'policy_output': 'categorical_crossentropy',
        'value_output': 'mse'
    },
    metrics={
        'policy_output': 'accuracy',
        'value_output': 'mse'
    }
)

# 8) Podemos inspeccionar la arquitectura
model_othello.summary()
