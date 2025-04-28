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

def apostar_paroli(apuesta_actual, gano):
    if gano:
        if apuesta_actual < 80:
            return apuesta_actual * 2
        else:
            return 10
    else:
        return 10

def estrategia(apuesta_actual, historial, gano, tipo):
    if tipo == 'm':
        return apostar_martingala(apuesta_actual, gano), historial
    elif tipo == 'd':
        return apostar_dalembert(apuesta_actual, gano), historial
    elif tipo == 'f':
        nueva_apuesta, historial = apostar_fibonacci(historial, gano)
        return nueva_apuesta, historial
    elif tipo == 'o':
        return apostar_paroli(apuesta_actual, gano), historial
    else:
        raise ValueError("Estrategia no reconocida")

def get_row(number):
    if number == 0:
        return None
    if number % 3 == 1:
        return "primera"
    elif number % 3 == 2:
        return "segunda"
    else:
        return "tercera"

def get_dozen(number):
    if 1 <= number <= 12:
        return "primera docena"
    elif 13 <= number <= 24:
        return "segunda docena"
    elif 25 <= number <= 36:
        return "tercera docena"
    else:
        return None

def odd_even(number):
    if number == 0:
        return None
    return "par" if number % 2 == 0 else "impar"

def red_black(number):
    if number == 0:
        return None
    if number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
        return "rojo"
    else:
        return "negro"

def jugar(tiradas, numero_elegido, tipo_estrategia, capital_tipo, capital_inicial):
    capital = capital_inicial
    apuesta = 10
    historial_apuestas = []
    capital_historial = []
    banca_rota = False

    for i in range(tiradas):
        if capital >= apuesta or capital_tipo == 'i':
            resultado = simular_ruleta()
            gano = False

            if numero_elegido in ['f1', 'f2', 'f3']:
                if (get_row(resultado) == {'f1': 'primera', 'f2': 'segunda', 'f3': 'tercera'}[numero_elegido]):
                    gano = True
            elif numero_elegido in ['d1', 'd2', 'd3']:
                if (get_dozen(resultado) == {'d1': 'primera docena', 'd2': 'segunda docena', 'd3': 'tercera docena'}[numero_elegido]):
                    gano = True
            elif numero_elegido == 'p':
                if odd_even(resultado) == 'par':
                    gano = True
            elif numero_elegido == 'i':
                if odd_even(resultado) == 'impar':
                    gano = True
            elif numero_elegido == 'r':
                if red_black(resultado) == 'rojo':
                    gano = True
            elif numero_elegido == 'n':
                if red_black(resultado) == 'negro':
                    gano = True
            elif numero_elegido == '0':
                if resultado == 0:
                    gano = True
            else:
                try:
                    if resultado == int(numero_elegido):
                        gano = True
                except:
                    raise ValueError("Número elegido no válido")

            if gano:
                if numero_elegido in ['f1', 'f2', 'f3', 'd1', 'd2', 'd3']:
                    capital += apuesta * 2
                elif numero_elegido in ['p', 'i', 'r', 'n']:
                    capital += apuesta
                else:
                    capital += apuesta * 35
            else:
                capital -= apuesta

            apuesta, historial_apuestas = estrategia(apuesta, historial_apuestas, gano, tipo_estrategia)
            if capital_tipo == 'i' and capital <= 0:
                capital = 10
        else:
            banca_rota = True
            break

        capital_historial.append(capital)

    while len(capital_historial) < tiradas:
        capital_historial.append(capital)

    return capital_historial, banca_rota

def graficar_capital(capital_historial, titulo, nombre_archivo):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(capital_historial)+1), capital_historial, color='red')
    plt.axhline(y=capital_historial[0], color='blue', linestyle='--', label='Capital Inicial')
    plt.title(titulo)
    plt.xlabel("Tiradas")
    plt.ylabel("Capital")
    plt.grid(True)
    plt.legend()
    plt.savefig(nombre_archivo)
    plt.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, default=1, help="Número de corridas")
    parser.add_argument("-n", "--tiradas", type=int, default=1000, help="Número de tiradas por corrida")
    parser.add_argument("-e", "--elegido", type=str, default='17', help="Número elegido")
    parser.add_argument("-s", "--estrategia", type=str, required=True, help="Estrategia: m (martingala), d (D'Alembert), f (Fibonacci), o (otra)")
    parser.add_argument("-a", "--capital", type=str, required=True, help="Capital: f (finito), i (infinito)")
    parser.add_argument("-i", "--inicial", type=int, default=1000, help="Capital inicial")
    args = parser.parse_args()

    banca_rotas = 0

    for i in range(args.corridas):
        capital_historial, banca_rota = jugar(args.tiradas, args.elegido, args.estrategia, args.capital, args.inicial)
        graficar_capital(capital_historial, f"Corrida {i+1} - Evolución del Capital", f"capital_corrida_{i+1}.png")
        if banca_rota:
            banca_rotas += 1

    print(f"Simulación finalizada.")
    print(f"Resultados de la estrategia '{args.estrategia}' con capital '{args.capital}':")
    print(f"Capital inicial: {args.inicial}")
    print(f"Número elegido: {args.elegido}")
    print(f"Número de tiradas por corrida: {args.tiradas}")
    print(f"Número de corridas: {args.corridas}")
    print(f"Total de bancarrotas: {banca_rotas} de {args.corridas} corridas.")

if __name__ == "__main__":
    main()