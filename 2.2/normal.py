import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# --- Densidad de la normal estándar ---
def f_normal(x):
    return (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)


# --- Método de rechazo ---
def generar_normal_rechazo(n, a=-5, b=5):
    samples = []
    M = f_normal(0) * (b - a)  # Cota superior para la función
    while len(samples) < n:
        x = np.random.uniform(a, b)
        u = np.random.uniform(0, M)
        if u <= f_normal(x):
            samples.append(x)
    return np.array(samples)


# --- Método de la transformada inversa ---
def generar_normal_inversa(n):
    u = np.random.uniform(0, 1, size=n)
    z = norm.ppf(u)  # Inversa de la CDF de N(0,1)
    return z


# --- Función para graficar y mostrar estadísticas ---
def graficar_distribucion(metodo, n=10000):
    if metodo == 'rechazo':
        datos = generar_normal_rechazo(n)
        nombre = "Método de Rechazo"
    elif metodo == 'inversa':
        datos = generar_normal_inversa(n)
        nombre = "Transformación Inversa"
    else:
        raise ValueError("Método no reconocido. Usa 'rechazo' o 'inversa'.")

    media = np.mean(datos)
    std = np.std(datos)

    print(f"[{nombre}] Media estimada: {media:.4f} (esperada: 0)")
    print(f"[{nombre}] Desviación estándar estimada: {std:.4f} (esperada: 1)")

    plt.hist(datos, bins=50, density=True, color='lightblue',
             edgecolor='black', alpha=0.7, label='Muestras')
    x = np.linspace(-5, 5, 1000)
    plt.plot(x, f_normal(x), 'r-', lw=2, label='N(0,1) teórica')
    plt.title(f"Distribución Normal - {nombre}")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"2.2/visualizaciones/normal_{metodo}.png", )



# --- Ejecución principal ---
if __name__ == "__main__":
    graficar_distribucion(metodo='rechazo', n=10000)
    graficar_distribucion(metodo='inversa', n=10000)
