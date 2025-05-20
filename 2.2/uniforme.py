import numpy as np
import math
import matplotlib.pyplot as plt
import random

# Transformada inversa

def generar_uniforme_inversa(a, b, n):
    u = np.random.random(n)
    return a + (b - a) * u

def generar_uniforme_rechazo(a, b, c=1.1):
    if a >= b:
        raise ValueError("El límite inferior 'a' debe ser menor que el límite superior 'b'")
    if c <= 1:
        raise ValueError("La constante 'c' debe ser mayor que 1")

    f = 1 / (b - a)  

    while True:
        x = random.uniform(a, b)           # candidato x ~ g(x)
        u = random.uniform(0, c * f)       # u ~ U(0, c*f(x))

        if u <= f:
            return x  


def test_uniforme(a, b, n=10000):
    datos = generar_uniforme_inversa(a, b, n)
    media = np.mean(datos)
    varianza = np.var(datos)
    print(f"Media estimada: {media:.4f} (esperada: {(a + b)/2:.4f})")
    print(f"Varianza estimada: {varianza:.4f} (esperada: {(b - a)**2 / 12:.4f})")

    # Histograma con ajustes estéticos
    plt.figure(figsize=(8, 5))
    count, bins, ignored = plt.hist(
        datos, bins=30, range=(a, b), density=True,
        color='mediumseagreen', edgecolor='black', alpha=0.75, label="Histograma"
    )

    # Densidad teórica uniforme
    plt.hlines(1 / (b - a), xmin=a, xmax=b, colors='red', linestyles='dashed', label='Densidad teórica')

    plt.title(f'Distribución Uniforme U({a},{b}) - Transformada Inversa')
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    test_uniforme(a=2, b=5, n=10000)