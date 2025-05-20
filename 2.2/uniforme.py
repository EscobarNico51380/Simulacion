import numpy as np
import math
import matplotlib.pyplot as plt
import random

# Transformada inversa

def generar_uniforme_inversa(a, b, n):
    u = np.random.random(n)
    return a + (b - a) * u

def generar_uniforme_rechazo(a, b, n, c=1.1):
    if a >= b:
        raise ValueError("El límite inferior 'a' debe ser menor que el límite superior 'b'")
    if c <= 1:
        raise ValueError("La constante 'c' debe ser mayor que 1")

    f = 1 / (b - a)
    results = []

    for _ in range(n):
        while True:
            x = random.uniform(a, b)
            u = random.uniform(0, c * f)
            if u <= f:
                results.append(x)
                break

    return np.array(results)


def graficar_uniforme(metodo, a, b, n=10000):
    if metodo == 'inversa':
        datos = generar_uniforme_inversa(a, b, n)
        nombre = "Transformada Inversa"
    elif metodo == 'rechazo':
        datos = generar_uniforme_rechazo(a, b, n)
        nombre = "Método de Rechazo"
    else:
        raise ValueError("Método no reconocido. Usa 'inversa' o 'rechazo'.")

    media = np.mean(datos)
    varianza = np.var(datos)
    media_teo = (a + b) / 2
    var_teo = (b - a) ** 2 / 12

    print(f"[{nombre}] Media estimada: {media:.4f} (esperada: {media_teo:.4f})")
    print(f"[{nombre}] Varianza estimada: {varianza:.4f} (esperada: {var_teo:.4f})")

    # Histograma con densidad teórica
    plt.figure(figsize=(8, 5))
    plt.hist(datos, bins=30, range=(a, b), density=True,
             color='cornflowerblue' if metodo == 'rechazo' else 'mediumseagreen',
             edgecolor='black', alpha=0.75, label="Histograma")

    plt.hlines(1 / (b - a), xmin=a, xmax=b,
               colors='red', linestyles='dashed', label='Densidad teórica')

    plt.title(f'Distribución Uniforme U({a},{b}) - {nombre}')
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"2.2/visualizaciones/uniforme_{metodo}.png", )


if __name__ == "__main__":
    graficar_uniforme(metodo='inversa', a=2, b=5, n=10000)
    graficar_uniforme(metodo='rechazo', a=2, b=5, n=10000)