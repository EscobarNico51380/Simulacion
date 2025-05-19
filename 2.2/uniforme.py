import numpy as np
import math
import matplotlib.pyplot as plt

def generar_uniforme(a, b, n):
    u = np.random.random(n)
    return a + (b - a) * u

def test_uniforme(a, b, n=10000):
    datos = generar_uniforme(a, b, n)
    media = np.mean(datos)
    print(f"Media estimada: {media:.4f} (esperada: {(a + b)/2:.4f})")

    plt.hist(datos, bins=50, density=True, color='lightgreen', edgecolor='black')
    plt.title(f"Histograma Uniforme U({a},{b})")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_uniforme(a=2, b=5, n=10000)