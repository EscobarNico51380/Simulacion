import random
import math
import matplotlib.pyplot as plt
import numpy as np

# ----------- Funciones dadas ----------- #
def pmf_pascal(x, r, p):
    if x < 0:
        return 0
    return math.comb(x + r - 1, x) * (p ** r) * ((1 - p) ** x)

def pmf_geom(x, q):
    if x < 0:
        return 0
    return (1 - q) * (q ** x)

def rechazo_pascal(r, p):
    if r <= 0 or not isinstance(r, int):
        raise ValueError("r debe ser un entero positivo")
    if not (0 < p < 1):
        raise ValueError("p debe estar en el intervalo (0, 1)")

    q = 1 - 0.5 * p
    c = 0
    for x in range(100):
        fx = pmf_pascal(x, r, p)
        gx = pmf_geom(x, q)
        if gx > 0:
            c = max(c, fx / gx)

    while True:
        u = random.random()
        x = int(math.log(1 - u) / math.log(q))

        fx = pmf_pascal(x, r, p)
        gx = pmf_geom(x, q)
        if gx == 0:
            continue

        u2 = random.uniform(0, 1)
        if u2 <= fx / (c * gx):
            return x

# ----------- Parámetros de la distribución ----------- #
r = 5       # número de éxitos
p = 0.4     # probabilidad de éxito
n_muestras = 10000

# ----------- Generar muestras ----------- #
muestras = [rechazo_pascal(r, p) for _ in range(n_muestras)]

# ----------- Estadísticas empíricas ----------- #
media_emp = np.mean(muestras)
varianza_emp = np.var(muestras)

# ----------- Estadísticas teóricas ----------- #
media_esp = r * (1 - p) / p
varianza_esp = r * (1 - p) / (p ** 2)

# ----------- Mostrar resultados ----------- #
print("--- Testeo Pascal (rechazo) ---")
print(f"Media empírica: {media_emp:.4f} (teórica: {media_esp:.4f})")
print(f"Varianza empírica: {varianza_emp:.4f} (teórica: {varianza_esp:.4f})")

# ----------- Graficar histograma ----------- #
valores = range(min(muestras), max(muestras) + 1)
frecuencias_emp = [muestras.count(k) / n_muestras for k in valores]
frecuencias_teor = [pmf_pascal(k, r, p) for k in valores]

plt.bar(valores, frecuencias_emp, width=0.8, alpha=0.6, label='Empírica', color='skyblue', edgecolor='black')
plt.plot(valores, frecuencias_teor, 'ro-', label='Teórica')

plt.title('Distribución Pascal (binomial negativa) - Método de rechazo')
plt.xlabel('x (fallos hasta r éxitos)')
plt.ylabel('Probabilidad')
plt.legend()
plt.grid(True)
plt.show()
