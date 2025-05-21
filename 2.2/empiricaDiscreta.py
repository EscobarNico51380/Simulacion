import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def rechazo_empirico_discreto(valores, probabilidades):
    """
    Genera un valor de una distribución empírica discreta usando el método de rechazo.
    
    :param valores: lista de valores posibles
    :param probabilidades: lista de probabilidades asociadas
    :return: un valor aleatorio según la distribución dada
    """
    if not (len(valores) == len(probabilidades)):
        raise ValueError("Las listas de valores y probabilidades deben tener la misma longitud.")

    if not np.isclose(sum(probabilidades), 1.0):
        raise ValueError("Las probabilidades deben sumar 1.")

    n = len(valores)
    g = 1 / n  # uniforme discreta
    c = max(probabilidades) / g  # constante de mayoración

    while True:
        i = random.randint(0, n - 1)  # índice según g(x) = uniforme
        u = random.uniform(0, c * g)

        if u <= probabilidades[i]:
            return valores[i]


# Distribución empírica
valores = [1, 2, 3, 4]
probabilidades = [0.1, 0.3, 0.4, 0.2]

# Generar muestras
muestras = [rechazo_empirico_discreto(valores, probabilidades) for _ in range(10000)]

# Contar frecuencia relativa
conteo = Counter(muestras)
frecuencia = [conteo[v] / len(muestras) for v in valores]

# Graficar
plt.bar([str(v) for v in valores], frecuencia, label="Frec. observada", alpha=0.6)
plt.plot([str(v) for v in valores], probabilidades, label="Prob. teórica", color='red', marker='o')
plt.title("Distribución generada por rechazo")
plt.ylabel("Frecuencia")
plt.legend()
plt.grid(True)
plt.show()
#plt.savefig("2.2/visualizaciones/empirica_discreta_rechazo.png", )

