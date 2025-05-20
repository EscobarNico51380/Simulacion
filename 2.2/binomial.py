import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, chisquare, kstest

# Parámetros de la binomial y tamaño de muestra
n = 10        # número de ensayos
p = 0.5       # probabilidad de éxito
N = 10000     # tamaño de muestra

def binomial_pmf(k, n, p):
    """Devuelve P(X=k) para X ~ Binomial(n, p)."""
    return binom.pmf(k, n, p)

# --- Cálculo de c para el método de rechazo ---
prob_vals = [binomial_pmf(k, n, p) for k in range(n + 1)]
c = (n + 1) * max(prob_vals)

# --- Generación de muestras vía método de rechazo ---
samples = []
while len(samples) < N:
    k = np.random.randint(0, n + 1)    # propuesta uniforme en {0,...,n}
    u = np.random.uniform(0, 1)        # U(0,1)
    if u < (n + 1) * binomial_pmf(k, n, p) / c:
        samples.append(k)

samples = np.array(samples)

# --- Cálculo de estadísticas empíricas ---
mean_emp = samples.mean()
var_emp  = samples.var(ddof=0)  # varianza poblacional (ddof=0)

# Teóricas para B(n, p)
mean_theo = n * p
var_theo  = n * p * (1 - p)

# --- Histograma alineado + superposición teórica ---
plt.figure(figsize=(8, 5))
plt.hist(samples,
         bins=np.arange(n + 2),
         density=True,
         alpha=0.6,
         label="Generado",
         align='left')
x = np.arange(0, n + 1)
plt.plot(x,
         binom.pmf(x, n, p),
         'o-',
         label="Binomial teórica")
plt.xlabel("k")
plt.ylabel("Probabilidad")
plt.title("Método de rechazo para $B(10, 0.5)$")
plt.legend()
plt.tight_layout()
plt.savefig("2.2/visualizaciones/binomial_rechazo.png")

# --- Test Chi-cuadrado ---
observed_freqs = np.bincount(samples, minlength=n+1)
expected_freqs = N * binomial_pmf(x, n, p)
chi2_stat, p_value_chi2 = chisquare(f_obs=observed_freqs, f_exp=expected_freqs)

# --- Test Kolmogorov-Smirnov (con CDF escalonada) ---
# Importante: usar la función acumulada teórica como callable
ks_stat, p_value_ks = kstest(samples, cdf=lambda k: binom.cdf(k, n, p))

# --- Impresiones finales ---
print(f"Media empírica: {mean_emp:.4f} (teórica: {mean_theo:.4f})")
print(f"Varianza empírica: {var_emp:.4f} (teórica: {var_theo:.4f})")
print(f"Chi-cuadrado: {chi2_stat:.2f}, p-value: {p_value_chi2:.4f}")
print(f"Kolmogorov-Smirnov: {ks_stat:.4f}, p-value: {p_value_ks:.4f}")
