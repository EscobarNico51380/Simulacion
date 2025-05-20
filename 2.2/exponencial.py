import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, kstest

def generar_exponencial_inversa(lambd, n):
    u = np.random.random(n)
    return -np.log(u) / lambd

def generar_exponencial_rechazo(lambd, n, x_max=10):
    datos = []
    while len(datos) < n:
        x = np.random.uniform(0, x_max)
        y = np.random.uniform(0, lambd)  
        if y <= lambd * np.exp(-lambd * x):
            datos.append(x)
    return np.array(datos)


def testeo_exponencial(datos, lambd, metodo):
    media_emp = np.mean(datos)
    var_emp = np.var(datos)
    media_teo = 1 / lambd
    var_teo = 1 / (lambd ** 2)

    print(f"--- Testeo {metodo} ---")
    print(f"Media empírica: {media_emp:.4f} (teórica: {media_teo:.4f})")
    print(f"Varianza empírica: {var_emp:.4f} (teórica: {var_teo:.4f})")

    # KS test
    d_stat, p_valor = kstest(datos, 'expon', args=(0, 1/lambd))
    print(f"Kolmogorov-Smirnov D: {d_stat:.4f}, p-valor: {p_valor:.4f}")

    # Histograma
    plt.hist(datos, bins=50, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    x = np.linspace(0, max(datos), 200)
    plt.plot(x, lambd * np.exp(-lambd * x), 'r--', label='f(x) teórica')
    plt.title(f"Histograma Exponencial ({metodo})")
    plt.xlabel("x")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    np.random.seed(42)
    lambd = 1.5
    n = 10000

    # Método inversa
    datos_inv = generar_exponencial_inversa(lambd, n)
    testeo_exponencial(datos_inv, lambd, "Transformada Inversa")

    # Método de rechazo
    datos_rej = generar_exponencial_rechazo(lambd, n)
    testeo_exponencial(datos_rej, lambd, "Rechazo")