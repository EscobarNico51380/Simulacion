
from math import exp, factorial
import random
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from scipy.stats import poisson

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
    # Primero calculamos el máximo valor de pmf para Poisson en [0, k_max]
    # que será el valor de la función en la moda (aproximadamente floor(lam))
    k_mode = int(lam)
    pmf_max = pmf_poisson(k_mode, lam)
    
    while True:
        # Proponemos un candidato k_uniform en 0..k_max (discreto uniforme)
        k_cand = random.randint(0, k_max)
        
        # Proponemos un valor u uniforme para aceptar/rechazar
        u = random.uniform(0, pmf_max)
        
        if u <= pmf_poisson(k_cand, lam):
            return k_cand

def generar_muestras_poisson(lam, n):
    return [generar_poisson_rechazo(lam) for _ in range(n)]

def testear_poisson_histograma(lam, n):
    datos = generar_muestras_poisson(lam, n)
    conteo = Counter(datos)
    valores = sorted(conteo.keys())
    frecuencias_empiricas = [conteo[v] / n for v in valores]

    valores_teoricos = np.arange(0, max(valores) + 1)
    pmf_teorica = poisson.pmf(valores_teoricos, lam)

    plt.bar(valores, frecuencias_empiricas, width=0.6, label='Empírica', alpha=0.7)
    plt.plot(valores_teoricos, pmf_teorica, 'ro-', label='Teórica (PMF)', markersize=5)
    plt.title(f"Distribución de Poisson(λ={lam}) - Histograma vs PMF (Rechazo)")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"2.2/visualizaciones/poisson_rechazo.png", )


if __name__ == "__main__":
    lam = 4
    n = 10000
    testear_poisson_histograma(lam, n)

