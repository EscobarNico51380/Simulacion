import argparse
import numpy as np
import random
from scipy.stats import chisquare, kstest

# GENERADORES

def gcl(seed, a, c, m, n):
    """Generador Congruencial Lineal"""
    x = seed
    numeros = []
    for _ in range(n):
        x = (a * x + c) % m
        numeros.append(x / m)
    return numeros

def cuadrados_medios(seed, n):
    """Método de los Cuadrados Medios"""
    numeros = []
    x = seed
    for _ in range(n):
        x = int(str(x**2).zfill(8)[2:6])  # extraer dígitos centrales
        numeros.append(x / 10000)  # normalizar
    return numeros

def python_random(n):
    return [random.random() for _ in range(n)]

# TESTS ESTADÍSTICOS

def media_varianza_test(nums):
    media = np.mean(nums)
    varianza = np.var(nums)
    return media, varianza

def chi_cuadrado_test(nums, bins=10):
    freq, _ = np.histogram(nums, bins=bins, range=(0, 1))
    esperada = len(nums) / bins
    chi2, p = chisquare(freq, f_exp=[esperada]*bins)
    return chi2, p

def kolmogorov_smirnov_test(nums):
    d, p = kstest(nums, 'uniform')
    return d, p

def autocorrelacion_test(nums, lag=1):
    n = len(nums)
    x = np.array(nums)
    x_mean = np.mean(x)
    num = np.sum((x[:n-lag] - x_mean) * (x[lag:] - x_mean))
    den = np.sum((x - x_mean)**2)
    r = num / den
    return r

# MAIN


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", type=int, default=1234, help="Número de seed")
    parser.add_argument("-n", "--n", type=int, default=10000, help="Número de corridas")
    args = parser.parse_args()
    seed = args.seed
    n = args.n
    print(f"Using random seed: {seed}")

    # GCL params
    a = 1664525
    c = 1013904223
    m = 2**32

    gcl_nums = gcl(seed, a, c, m, n)
    cuad_nums = cuadrados_medios(seed, n)
    py_nums = python_random(n)

    generadores = {
        "GCL": gcl_nums,
        "Cuadrados Medios": cuad_nums,
        "Python": py_nums
    }

    for nombre, nums in generadores.items():
        print(f"\n--- Resultados para {nombre} ---")
        media, varianza = media_varianza_test(nums)
        chi2, p_chi = chi_cuadrado_test(nums)
        d, p_ks = kolmogorov_smirnov_test(nums)
        r = autocorrelacion_test(nums)

        print(f"Media: {media:.4f}, Varianza: {varianza:.4f}")
        print(f"Chi²: {chi2:.2f}, p-valor: {p_chi:.4f}")
        print(f"KS D: {d:.4f}, p-valor: {p_ks:.4f}")
        print(f"Autocorrelación (lag 1): {r:.4f}")
