from math import exp, factorial
import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import poisson, kstest, chisquare

def pmf_poisson(k, lam):
    """
    Función masa de probabilidad de Poisson
    """
    return (lam ** k) * exp(-lam) / factorial(k)

def generar_poisson_rechazo(lam, k_max=100):
    """
    Genera una variable aleatoria con distribución Poisson usando el método del rechazo.
    
    Parámetros:
    lam : media esperada λ de la distribución Poisson
    k_max : valor máximo para k en el soporte (para limitar la búsqueda)
    
    Retorna:
    Un entero con distribución Poisson(λ)
    """
    
    k_max = int(poisson.ppf(0.999, lam)) # Adaptar k_max dinámicamente al percentil 99.9 de la Poisson(λ), para evitar valores extremos y evitar sesgo
    k_mode = int(lam)
    pmf_max = pmf_poisson(k_mode, lam)
    
    while True:
        k_cand = random.randint(0, k_max)
        u = random.uniform(0, pmf_max)
        
        if u <= pmf_poisson(k_cand, lam):
            return k_cand

def generar_muestras_poisson(lam, n):
    return [generar_poisson_rechazo(lam) for _ in range(n)]

def testear_poisson_histograma(lam, n):
    datos = generar_muestras_poisson(lam, n)
    conteo = Counter(datos)
    valores = sorted(conteo.keys())
    frecuencias_empiricas = np.array([conteo[v] for v in valores])

    # PMF y frecuencias esperadas para Chi-cuadrado
    pmf_teorica = poisson.pmf(valores, lam)
    frecuencias_esperadas = pmf_teorica * n

    plt.bar(valores, frecuencias_empiricas / n, width=0.6, label='Empírica', alpha=0.7)
    valores_teoricos = np.arange(0, max(valores) + 1)
    pmf_teorica_full = poisson.pmf(valores_teoricos, lam)
    plt.plot(valores_teoricos, pmf_teorica_full, 'ro-', label='Teórica (PMF)', markersize=5)
    plt.title(f"Distribución de Poisson(λ={lam}) - Histograma vs PMF (Rechazo)")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"2.2/visualizaciones/poisson_rechazo2.png")

    # Test KS
    stat_ks, p_value_ks = kstest(datos, 'poisson', args=(lam,))
    print(f"Test KS: estadístico D = {stat_ks:.4f}, p-valor = {p_value_ks:.4f}")
    if p_value_ks > 0.05:
        print("✅ No se rechaza H0: los datos siguen una distribución Poisson.")
    else:
        print("❌ Se rechaza H0: los datos NO siguen una distribución Poisson.")

    # Test Chi-cuadrado
    # Agrupamos en categorías para que las frecuencias esperadas no sean muy pequeñas:
    # Esto es importante, aquí solo hago un agrupamiento simple para frecuencias < 5
    obs = list(frecuencias_empiricas)
    exp = list(frecuencias_esperadas)

    # Agrupar cola derecha para frecuencias esperadas < 5
    while exp[-1] < 5:
        exp[-2] += exp[-1]
        obs[-2] += obs[-1]
        exp = exp[:-1]
        obs = obs[:-1]

    exp = np.array(exp)
    obs = np.array(obs)

    # Normalizar exp para igualar suma a obs (por posibles errores de redondeo)
    exp = exp * (obs.sum() / exp.sum())

    stat_chi, p_value_chi = chisquare(f_obs=obs, f_exp=exp)

    print(f"Test Chi-cuadrado: estadístico χ² = {stat_chi:.4f}, p-valor = {p_value_chi:.4f}")
    if p_value_chi > 0.05:
        print("✅ No se rechaza H0: los datos siguen una distribución Poisson.")
    else:
        print("❌ Se rechaza H0: los datos NO siguen una distribución Poisson.")

if __name__ == "__main__":
    lam = 4
    n = 10000
    testear_poisson_histograma(lam, n)
