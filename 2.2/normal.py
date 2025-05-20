import numpy as np
import matplotlib.pyplot as plt




def f_normal(x):
    return (1/np.sqrt(2*np.pi)) * np.exp(-x**2 / 2)

def generar_normal_rechazo(n, a=-5, b=5):
    samples = []
    M = f_normal(0) * (b - a)
    while len(samples) < n:
        x = np.random.uniform(a, b)
        u = np.random.uniform(0, M)
        if u <= f_normal(x):
            samples.append(x)
    return np.array(samples)

def test_normal_rechazo(n=10000):
    datos = generar_normal_rechazo(n)
    media = np.mean(datos)
    std = np.std(datos)
    print(f"[Rechazo] Media estimada: {media:.4f} (esperada: 0)")
    print(f"[Rechazo] Desviación estándar estimada: {std:.4f} (esperada: 1)")

    plt.hist(datos, bins=50, density=True, color='lightblue', edgecolor='black', alpha=0.7, label='Muestras')
    x = np.linspace(-5, 5, 1000)
    plt.plot(x, f_normal(x), 'r-', lw=2, label='N(0,1) teórica')
    plt.title("Distribución Normal por Método de Rechazo")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_normal_rechazo(n=10000)
