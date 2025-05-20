import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, kstest

# 1. Parámetros de la distribución objetivo (Gamma)
k = 2.0       # parámetro de forma
theta = 2.0   # parámetro de escala
a = 0         # límite inferior del intervalo de búsqueda
b = 20        # límite superior (acotar la cola de la gamma)
N = 10000     # cantidad de muestras deseadas

# 2. Definir f(x): función de densidad objetivo (Gamma)
def f(x):
    return gamma.pdf(x, a=k, scale=theta)

def g(x0, c):
    return f(x0) / c # normaliza f(x) para que devuelva valores entre [0,1]

# 3. Calcular c = max f(x) en [a,b]
x_vals = np.linspace(a, b, 1000)
c = np.max(f(x_vals))  # c ≥ f(x) ∀ x ∈ [a,b]

# 4. g(x) = f(x)/c → f(x)/c ∈ [0,1] ahora sí
# Usamos distribución propuesta uniforme en [a, b]
samples = []

while len(samples) < N:
    r1 = np.random.random()  # número aleatorio en [0,1]
    x0 = a + (b - a) * r1     # valor candidato de X
    
    r2 = np.random.random()  # otro número aleatorio en [0,1]
    
    if r2 <= g(x0,c): # el punto (x0,r2) se acepta solo si cae debajo de la curva normalizada
        samples.append(x0)

samples = np.array(samples)

# 5. Graficar resultados
plt.hist(samples, bins=50, density=True, alpha=0.6, label='Muestra generada')
x = np.linspace(a, b, 1000)
plt.plot(x, f(x), 'r-', label='Gamma teórica')
plt.title('Método del rechazo para distribución Gamma')
plt.xlabel('x')
plt.ylabel('Densidad')
plt.legend()
plt.grid()
plt.show()

# 6. Prueba estadística (Kolmogorov-Smirnov)
stat, p_value = kstest(samples, 'gamma', args=(k, 0, theta))
print(f"KS statistic: {stat:.4f}, p-value: {p_value:.4f}")
if p_value > 0.05:
    print("✅ No se rechaza H0: los datos siguen una distribución gamma.")
else:
    print("❌ Se rechaza H0: los datos NO siguen una distribución gamma.")
