import math
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
        
        frecuencia_relativa.append(fr)
        promedio.append(prom)
        
        # Para cálculo de varianza y desviación estándar
        if i > 1:
            # Calculamos la varianza muestral
            var = sum((numeros_sorteados[j-1] - prom) ** 2 for j in range(i)) / (i - 1)
            desv = math.sqrt(var)  # Desviación estándar es la raíz cuadrada de la varianza
        else:
            var = 0  # No se puede calcular varianza con solo una observación
            desv = 0
            
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
    # La varianza de que un numero X salga en la ruleta sigue una ditribucion uniforme 
    varianzaEsperada = ((37**2)-1)/12
    desvioEsperado = math.sqrt(varianzaEsperada)
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, default=1, help="Número de corridas")
    parser.add_argument("-n", "--tiradas", type=int, default=1000, help="Número de tiradas por corrida")
    parser.add_argument("-e", "--elegido", type=int, default=17, help="Número elegido")
    args = parser.parse_args()

    corridas = args.corridas
    tiradas = args.tiradas
    numero_elegido = args.elegido

    numeros = simular_ruleta(tiradas)
    frn, vpn, vd, vv = calcular_estadisticas(numeros, numero_elegido)
    x = list(range(1, tiradas + 1))
    graficar(x, frn, 1 / 37, f"Una sola corrida - Frecuencia relativa del número {numero_elegido}", "Frecuencia relativa", f"grafica_frecuencia.png")
    graficar(x, vpn, 18, f"Una sola corrida  - Valor promedio de las tiradas", "Valor promedio", f"grafica_promedio.png")
    graficar(x, vd, desvioEsperado, f"Una sola corrida  - Desvío respecto al valor esperado", "Desvío", f"grafica_desvio.png")
    graficar(x,vv, varianzaEsperada, f"Una sola corrida  - Varianza respecto al valor esperado", "Varianza", f"grafica_varianza")

    print("Simulación finalizada. Gráficos guardados.")

    # Preparar listas para almacenar resultados de todas las corridas
    todas_frn = []
    todas_vpn = []
    todos_vd = []
    todos_vv = []
    
    # Realizar todas las corridas y almacenar resultados
    for i in range(corridas):
        numeros = simular_ruleta(tiradas)
        frn, vpn, vd, vv = calcular_estadisticas(numeros, numero_elegido)
        todas_frn.append(frn)
        todas_vpn.append(vpn)
        todos_vd.append(vd)
        todos_vv.append(vv)
    
    x = list(range(1, tiradas + 1))
    
    # Crear gráficas con todas las corridas superpuestas
    plt.figure(figsize=(10, 6))
    for i, frn in enumerate(todas_frn):
        plt.plot(x, frn, label=f"Corrida {i+1}", alpha=0.7)
    plt.axhline(y=1/37, color='black', linestyle='--', label="Esperado")
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("Frecuencia relativa")
    plt.title(f"Frecuencia relativa del número {numero_elegido} - {corridas} corridas")
    plt.legend()
    plt.grid(True)
    plt.savefig("grafica_frecuencia_todas.png")
    plt.close()
    
    plt.figure(figsize=(10, 6))
    for i, vpn in enumerate(todas_vpn):
        plt.plot(x, vpn, label=f"Corrida {i+1}", alpha=0.7)
    plt.axhline(y=18, color='black', linestyle='--', label="Esperado")
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("Valor promedio")
    plt.title(f"Valor promedio de las tiradas - {corridas} corridas")
    plt.legend()
    plt.grid(True)
    plt.savefig("grafica_promedio_todas.png")
    plt.close()
    
    plt.figure(figsize=(10, 6))
    for i, vd in enumerate(todos_vd):
        plt.plot(x, vd, label=f"Corrida {i+1}", alpha=0.7)
    plt.axhline(y=desvioEsperado, color='black', linestyle='--', label="Esperado")
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("Desvío")
    plt.title(f"Desvío respecto al valor esperado - {corridas} corridas")
    plt.legend()
    plt.grid(True)
    plt.savefig("grafica_desvio_todas.png")
    plt.close()
    
    plt.figure(figsize=(10, 6))
    for i, vv in enumerate(todos_vv):
        plt.plot(x, vv, label=f"Corrida {i+1}", alpha=0.7)
    plt.axhline(y=varianzaEsperada, color='black', linestyle='--', label="Esperado")
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("Varianza")
    plt.title(f"Varianza respecto al valor esperado - {corridas} corridas")
    plt.legend()
    plt.grid(True)
    plt.savefig("grafica_varianza_todas.png")
    plt.close()

if __name__ == "__main__":
    main()
