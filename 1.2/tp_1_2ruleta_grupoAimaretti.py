import math
import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

def simular_ruleta():
    return random.randint(0, 36)

def apostar_martingala(apuesta_actual, gano):
    return 10 if gano else apuesta_actual * 2

def apostar_dalembert(apuesta_actual, gano):
    return max(10, apuesta_actual - 10) if gano else apuesta_actual + 10

def apostar_fibonacci(historial_apuestas, gano):
    if not historial_apuestas:
        historial_apuestas = [10]
    if gano:
        historial_apuestas = historial_apuestas[:-2] if len(historial_apuestas) > 2 else [10]
    else:
        historial_apuestas.append(historial_apuestas[-1] + (historial_apuestas[-2] if len(historial_apuestas) > 1 else 0))
    return historial_apuestas[-1], historial_apuestas

def apostar_otra(apuesta_actual, gano):
    return 10 if gano else min(apuesta_actual * 1.5, 500)

def estrategia(apuesta_actual, historial, gano, tipo):
    if tipo == 'm':
        return apostar_martingala(apuesta_actual, gano), historial
    elif tipo == 'd':
        return apostar_dalembert(apuesta_actual, gano), historial
    elif tipo == 'f':
        nueva_apuesta, historial = apostar_fibonacci(historial, gano)
        return nueva_apuesta, historial
    elif tipo == 'o':
        return apostar_otra(apuesta_actual, gano), historial
    else:
        raise ValueError("Estrategia no reconocida")

def jugar(tiradas, numero_elegido, tipo_estrategia, capital_tipo, capital_inicial):
    capital = capital_inicial
    apuesta = 10
    historial_apuestas = []
    capital_historial = []
    banca_rota = False

    for i in range(tiradas):
        resultado = simular_ruleta()
        gano = (resultado == numero_elegido)

        if capital_tipo == 'f' and capital < apuesta:
            banca_rota = True
            break

        if gano:
            capital += apuesta * 35  # gana 35 veces la apuesta + la apuesta original
        else:
            capital -= apuesta

        apuesta, historial_apuestas = estrategia(apuesta, historial_apuestas, gano, tipo_estrategia)

        capital_historial.append(capital)

        if capital_tipo == 'f' and capital <= 0:
            banca_rota = True
            break

    return capital_historial, banca_rota

def graficar_capital(capital_historial, titulo, nombre_archivo):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(capital_historial)+1), capital_historial, color='red')
    plt.title(titulo)
    plt.xlabel("Tiradas")
    plt.ylabel("Capital")
    plt.grid(True)
    plt.savefig(nombre_archivo)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, default=1, help="Número de corridas")
    parser.add_argument("-n", "--tiradas", type=int, default=1000, help="Número de tiradas por corrida")
    parser.add_argument("-e", "--elegido", type=int, default=17, help="Número elegido")
    parser.add_argument("-s", "--estrategia", type=str, required=True, help="Estrategia: m (martingala), d (D'Alembert), f (Fibonacci), o (otra)")
    parser.add_argument("-a", "--capital", type=str, required=True, help="Capital: f (finito), i (infinito)")
    parser.add_argument("-i", "--inicial", type=int, default=1000, help="Capital inicial")
    args = parser.parse_args()

    corridas = args.corridas
    tiradas = args.tiradas
    numero_elegido = args.elegido
    tipo_estrategia = args.estrategia
    capital_tipo = args.capital
    capital_inicial = args.inicial

    banca_rotas = 0

    for i in range(corridas):
        capital_historial, banca_rota = jugar(tiradas, numero_elegido, tipo_estrategia, capital_tipo, capital_inicial)
        graficar_capital(capital_historial, f"Corrida {i+1} - Evolución del Capital", f"capital_corrida_{i+1}.png")
        if banca_rota:
            banca_rotas += 1

    print(f"Simulación finalizada.")
    print(f"Total de bancarrotas: {banca_rotas} de {corridas} corridas.")

if __name__ == "__main__":
    main()
