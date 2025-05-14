import argparse
import numpy as np
import random
from scipy.stats import chisquare, kstest
import matplotlib.pyplot as plt
import os

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

def guardar_visualizacion_bitmap(nums, nombre, size=(512, 512), carpeta="visualizaciones_prueba"):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Determinar el tamaño máximo posible según la cantidad de números disponibles
    total_elementos = len(nums)
    if total_elementos < size[0] * size[1]:
        # Ajustar el tamaño al número disponible de elementos
        lado = int(np.sqrt(total_elementos))
        size = (lado, lado)
        print(f"Advertencia: Ajustando bitmap a {size} debido a que hay solo {total_elementos} números")
    
    # Usar sólo los primeros size[0]*size[1] números
    data = np.array(nums[:size[0]*size[1]])

    # Convertir a blanco (1) y negro (0) usando un umbral de 0.5
    binarizado = np.where(data > 0.5, 1, 0)

    # Redimensionar en matriz 2D
    imagen = binarizado.reshape(size)

    # Guardar la imagen sin ejes ni bordes, estilo puro bitmap
    plt.figure(figsize=(6, 6), dpi=100)
    plt.imshow(imagen, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.savefig(f"{carpeta}/{nombre}_bitmap.png", bbox_inches='tight', pad_inches=0)
    plt.close()


# MAIN


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    # Se precisan 2 tipos de semilla dada la naturaleza de cada generador
    # En GCL la cantidad de digitos necesarios de la semilla puede decidirse a partir  del logaritmo en base 10 de m
    # Siendo en este caso log10(2**32)=9.63, luego precisariamos al menos 10 digitos. 
    parser.add_argument("--gcl-seed", type=int, default=1234567890, help="Semilla para GCL(10 digitos)")
    # Cuadrados medios usa de digitos 4
    parser.add_argument("--cuad-seed", type=int, default=1234, help="Semilla para Cuadrados Medios(4 digitos)")
    parser.add_argument("-n", "--n", type=int, default=10000, help="Número de corridas")
    args = parser.parse_args()
    
    GCLseed = args.gcl_seed
    cuad_seed = args.cuad_seed

    n = args.n
    print(f"Using GCL seed: {GCLseed}") # 0 ≤ seed < 4,294,967,296. Hasta 10 cifras
    print(f"Using Cuadrados_Medios seed: {cuad_seed}") #4 cifras
    

    # GCL params
    a = 1664525
    c = 1013904223
    m = 2**32

    if(len(str(GCLseed))!=10 or len(str(cuad_seed))!=4):
        print("Error: La semilla de GCL debe tener 10 digitos y la de cuadrados medios 4 digitos")
        exit(1)

    gcl_nums = gcl(GCLseed, a, c, m, n)
    cuad_nums = cuadrados_medios(cuad_seed, n)
    py_nums = python_random(n)
    

    generadores = {
        "GCL": gcl_nums,
        "Cuadrados_Medios": cuad_nums,
        "Python": py_nums
    }

    for nombre, nums in generadores.items():
        
        nums = np.array(nums, dtype=np.float32)

        print(f"\n--- Resultados para {nombre} ---")
        media, varianza = media_varianza_test(nums)
        chi2, p_chi = chi_cuadrado_test(nums)
        d, p_ks = kolmogorov_smirnov_test(nums)
        r = autocorrelacion_test(nums)

        print(f"Media: {media:.4f}, Varianza: {varianza:.4f}")
        print(f"Chi²: {chi2:.2f}, p-valor: {p_chi:.4f}")
        print(f"KS D: {d:.4f}, p-valor: {p_ks:.4f}")
        print(f"Autocorrelación (lag 1): {r:.4f}")

        guardar_visualizacion_bitmap(nums, f"{nombre}")

# python tp_2_1generadores_grupoAimaretti.py --gcl-seed 3129871234 --cuad-seed 5732 -n 100000000
# NOTA: Para correr n=100000000 se tiene que correr cada generador por separado, sino no da la memoria. Por lo menos a mi.
# Se usa ese n para poder ver los patrones en la imagen.
