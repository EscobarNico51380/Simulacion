import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom

# -------------------------------
# HIPERGEOMÉTRICA por MÉTODO DE RECHAZO
# -------------------------------

def generar_hipergeometrica_rechazo(N, K, n, muestras):
    """
    Método de rechazo para la distribución hipergeométrica.
    N = tamaño total de la población
    K = número total de éxitos en la población
    n = tamaño de la muestra extraída
    muestras = cantidad de valores a generar
    """
    
    valores = []
    min_k = max(0, n - (N - K))
    max_k = min(n, K)
    k_vals = np.arange(min_k, max_k + 1)
    max_prob = max(hypergeom.pmf(k_vals, N, K, n))

    
    while len(valores) < muestras:
        k_candidato = np.random.randint(min_k, max_k + 1)
        u = np.random.random()
        p_k = hypergeom.pmf(k_candidato, N, K, n)
        if u <= p_k / max_prob:
            valores.append(k_candidato)
    return np.array(valores)

# -------------------------------
# TESTEO
# -------------------------------

def testeo_hipergeometrica(valores, N, K, n):
    media_emp = np.mean(valores)
    var_emp = np.var(valores)
    media_teo = n * (K / N)
    var_teo = n * (K / N) * (1 - K / N) * (N - n) / (N - 1)

    print(f"--- Testeo Hipergeométrica (rechazo) ---")
    print(f"Media empírica: {media_emp:.4f} (teórica: {media_teo:.4f})")
    print(f"Varianza empírica: {var_emp:.4f} (teórica: {var_teo:.4f})")

    # Histograma
    plt.hist(valores, bins=np.arange(min(valores), max(valores)+1)-0.5,
             edgecolor='black', alpha=0.7, density=True)
    x = np.arange(min(valores), max(valores)+1)
    y = hypergeom.pmf(x, N, K, n)
    plt.plot(x, y, 'ro--', label='PMF teórica')
    plt.title(f"Hipergeométrica (N={N}, K={K}, n={n}) - Método de Rechazo")
    plt.xlabel("k")
    plt.ylabel("Probabilidad")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# -------------------------------
# MAIN
# -------------------------------

if __name__ == "__main__":
    N = 50     # tamaño total
    K = 15     # éxitos
    n = 10     # muestras extraídas
    muestras = 10000

    datos = generar_hipergeometrica_rechazo(N, K, n, muestras)
    testeo_hipergeometrica(datos, N, K, n)
