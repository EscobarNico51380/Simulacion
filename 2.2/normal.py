import numpy as np
import matplotlib.pyplot as plt


# para esta distribucion usamos box-muller

def generar_normal(mu, sigma, n):
    u1 = np.random.random(n // 2)
    u2 = np.random.random(n // 2)

    z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)

    z = np.concatenate((z0, z1))
    x = mu + sigma * z
    return x



def test_normal(mu=0, sigma=1, n=10000):
    datos = generar_normal(mu, sigma, n)
    media = np.mean(datos)
    std = np.std(datos)
    print(f"Media estimada: {media:.4f} (esperada: {mu})")
    print(f"Desviación estándar estimada: {std:.4f} (esperada: {sigma})")

    plt.hist(datos, bins=50, density=True, color='plum', edgecolor='black')
    plt.title(f"Histograma Normal(μ={mu}, σ={sigma})")
    plt.xlabel("Valor")
    plt.ylabel("Densidad")
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    test_normal(mu=0, sigma=1, n=10000)
