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
    elif tipo == 'p':
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

    frsa = []
    aciertos = 0
    for i, c in enumerate(capital_historial):
        # Primer tirada
        if i == 0:
            frsa.append(1 if c > capital_inicial else 0)
            if c > capital_inicial:
                aciertos += 1
        # El resto de las tiradas
        else:
            #Compara contra el capital de la tirada anterior
            if capital_historial[i] > capital_historial[i-1]:
                aciertos += 1
            #Agrega la frecuencia relativa de aciertos de la tirada i al arreglo
            frsa.append(aciertos / (i + 1))
    print(frsa[4])
    return capital_historial, banca_rota, frsa

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
    
def graficar_frsa(frsa, titulo, nombre_archivo):
    plt.figure(figsize=(8, 5))
    plt.bar(range(1, len(frsa) + 1), frsa, color='salmon', edgecolor='blue')
    plt.title(titulo)
    plt.xlabel("n (número de tiradas)")
    plt.ylabel("frsa (frecuencia relativa)")
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(nombre_archivo)
    plt.close()

def graficar_todas_corridas(historiales_capital, titulo, nombre_archivo):
    plt.figure(figsize=(17, 10))
    for i, capital_historial in enumerate(historiales_capital):
        plt.plot(range(1, len(capital_historial) + 1), capital_historial, label=f"Corrida {i + 1}", alpha=0.7)
    plt.axhline(y=historiales_capital[0][0], color='blue', linestyle='--', label='Capital Inicial')
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
    parser.add_argument("-s", "--estrategia", type=str, required=True, help="Estrategia: m (martingala), d (D'Alembert), f (Fibonacci), p (Paroli)")
    parser.add_argument("-a", "--capital", type=str, required=True, help="Capital: f (finito), i (infinito)")
    parser.add_argument("-i", "--inicial", type=int, default=1000, help="Capital inicial")
    args = parser.parse_args()

    banca_rotas = 0
    historiales_capital = []

    for _ in range(args.corridas):
        capital_historial, banca_rota, frsa = jugar(args.tiradas, args.elegido, args.estrategia, args.capital, args.inicial)
        historiales_capital.append(capital_historial)
        if banca_rota or capital_historial[-1] <= 0:
            banca_rotas += 1

    graficar_capital(capital_historial, f"Corrida {args.corridas} - Evolución del Capital", f"capital_corrida_{args.corridas}_{args.estrategia}_{args.capital}.png")
    graficar_frsa(frsa, f"Corrida {args.corridas} - Frecuencia Relativa de Aciertos", f"frsa_corrida_{args.corridas}_{args.estrategia}_{args.capital}.png")
        
    
    graficar_todas_corridas(historiales_capital, "Evolución del Capital - Todas las Corridas", f"capital_todas_corridas_{args.estrategia}_{args.capital}.png")
    print(f"Simulación finalizada.")
    print(f"Resultados de la estrategia '{args.estrategia}' con capital '{args.capital}':")
    print(f"Capital inicial: {args.inicial}")
    print(f"Número elegido: {args.elegido}")
    print(f"Número de tiradas por corrida: {args.tiradas}")
    print(f"Número de corridas: {args.corridas}")
    print(f"Total de bancarrotas: {banca_rotas} de {args.corridas} corridas.")

if __name__ == "__main__":
    main()