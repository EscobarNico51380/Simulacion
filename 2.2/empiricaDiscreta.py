import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

def rechazo_empirico_discreto(valores, probabilidades):
    """
    Genera un valor de una distribución empírica discreta usando el método de rechazo.
    """
    if not (len(valores) == len(probabilidades)):
        raise ValueError("Las listas de valores y probabilidades deben tener la misma longitud.")

    if not np.isclose(sum(probabilidades), 1.0):
        raise ValueError("Las probabilidades deben sumar 1.")

    n = len(valores)
    g = 1 / n  # uniforme discreta
    c = max(probabilidades) / g  # constante de mayoración

    while True:
        i = random.randint(0, n - 1)  # índice según g(x)
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

# ========================
# TEST KS (manual)
# ========================
# Calcular F(x) empírica y F(x) teórica acumuladas
valores_ordenados = sorted(valores)
n = len(muestras)
empirical_cdf = []
theoretical_cdf = []
cum_empirical = 0
cum_theoretical = 0

for v in valores_ordenados:
    freq = conteo[v]
    p = probabilidades[valores.index(v)]
    cum_empirical += freq / n
    cum_theoretical += p
    empirical_cdf.append(cum_empirical)
    theoretical_cdf.append(cum_theoretical)

# Estadístico KS
D = max(abs(e - t) for e, t in zip(empirical_cdf, theoretical_cdf))
print(f"Test KS (manual): estadístico D = {D:.4f}")
# No se puede calcular un p-valor exacto aquí sin una tabla, pero podemos usar el umbral de significancia aproximado
ks_threshold = 1.36 / np.sqrt(n)  # para alfa = 0.05

if D < ks_threshold:
    print("✅ No se rechaza H0: los datos siguen la distribución empírica especificada.")
else:
    print("❌ Se rechaza H0: los datos NO siguen la distribución empírica especificada.")

# ========================
# TEST CHI-CUADRADO
# ========================
# Frecuencias observadas y esperadas
obs = [conteo[v] for v in valores]
exp = [p * len(muestras) for p in probabilidades]

# Agrupamiento si alguna frecuencia esperada < 5
while any(e < 5 for e in exp):
    # fusionar dos últimos
    exp[-2] += exp[-1]
    obs[-2] += obs[-1]
    exp = exp[:-1]
    obs = obs[:-1]

# Normalización por redondeo
exp = np.array(exp)
obs = np.array(obs)
exp = exp * (obs.sum() / exp.sum())

stat_chi, p_value_chi = chisquare(f_obs=obs, f_exp=exp)

print(f"Test Chi-cuadrado: estadístico χ² = {stat_chi:.4f}, p-valor = {p_value_chi:.4f}")
if p_value_chi > 0.05:
    print("✅ No se rechaza H0: los datos siguen la distribución empírica especificada.")
else:
    print("❌ Se rechaza H0: los datos NO siguen la distribución empírica especificada.")
