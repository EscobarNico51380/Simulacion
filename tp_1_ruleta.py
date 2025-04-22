import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

def simular_ruleta(tiradas):
    numeros_sorteados = []
    for _ in range(tiradas):
        resultado = random.randint(0, 36)
        numeros_sorteados.append(resultado)
    return numeros_sorteados

def calcular_estadisticas(numeros_sorteados, numero_elegido):
    frecuencia_relativa = []
    promedio = []
    desviacion = []
    varianza = []

    conteo = 0
    suma = 0

    for i in range(1, len(numeros_sorteados) + 1):
        tirada = numeros_sorteados[i - 1]
        suma += tirada
        if tirada == numero_elegido:
            conteo += 1

        fr = conteo / i
        prom = suma / i
        desv = abs(fr - 1 / 37)
        var = (fr - 1 / 37) ** 2

        frecuencia_relativa.append(fr)
        promedio.append(prom)
        desviacion.append(desv)
        varianza.append(var)

    return frecuencia_relativa, promedio, desviacion, varianza

def graficar(x, y, valor_esperado, titulo, ylabel, nombre_archivo):
    plt.figure()
    plt.plot(x, y, label="Simulado", color='red')
    plt.axhline(y=valor_esperado, color='blue', linestyle='--', label="Esperado")
    plt.xlabel("n (número de tiradas)")
    plt.ylabel(ylabel)
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.savefig(nombre_archivo)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, default=1, help="Número de corridas")
    parser.add_argument("-n", "--tiradas", type=int, default=1000, help="Número de tiradas por corrida")
    parser.add_argument("-e", "--elegido", type=int, default=17, help="Número elegido")
    args = parser.parse_args()

    corridas = args.corridas
    tiradas = args.tiradas
    numero_elegido = args.elegido

    for corrida in range(corridas):
        numeros = simular_ruleta(tiradas)
        frn, vpn, vd, vv = calcular_estadisticas(numeros, numero_elegido)

        x = list(range(1, tiradas + 1))
        graficar(x, frn, 1 / 37, f"Corrida {corrida+1} - Frecuencia relativa del número {numero_elegido}", "Frecuencia relativa", f"grafica_frecuencia_{corrida+1}.png")
        graficar(x, vpn, 18, f"Corrida {corrida+1} - Valor promedio de las tiradas", "Valor promedio", f"grafica_promedio_{corrida+1}.png")
        graficar(x, vd, 0, f"Corrida {corrida+1} - Desvío respecto al valor esperado", "Desvío", f"grafica_desvio_{corrida+1}.png")
        graficar(x, vv, 0, f"Corrida {corrida+1} - Varianza respecto al valor esperado", "Varianza", f"grafica_varianza_{corrida+1}.png")

    print("Simulación finalizada. Gráficos guardados.")

if __name__ == "__main__":
    main()
