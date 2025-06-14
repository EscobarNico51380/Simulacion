import numpy as np
import matplotlib.pyplot as plt
import argparse
from collections import deque
import os


# Función que simula un sistema M/M/1 con cola finita o infinita
def simular_mm1(tasa_arribo, tasa_servicio, tamaño_maximo_cola=np.inf, tiempo_simulacion=1000):
    tiempo_ocupado = 0  # Tiempo total en el que el servidor estuvo ocupado
    t = 0  # Tiempo actual de simulación
    cola = deque()  # Cola de espera (estructura eficiente tipo FIFO)
    servidor_ocupado = False  # Estado del servidor: True si está atendiendo
    proxima_llegada = np.random.exponential(1 / tasa_arribo)  # Tiempo hasta la próxima llegada (distribución exponencial)
    proxima_salida = np.inf  # No hay salida programada al principio
    area_en_sistema = 0  # Área bajo la curva de "clientes en el sistema", para el promedio
    area_en_cola = 0  # Área bajo la curva de "clientes en cola", para el promedio
    tiempo_ultimo_evento = 0
    rechazados = 0  # Contador de clientes rechazados por cola llena
    tiempos_en_sistema = []  # Lista de los tiempos individuales que cada cliente pasó en el sistema

    # Bucle principal de simulación, avanza el tiempo hasta que se completa la simulación
    while t < tiempo_simulacion:
        # Avanza el tiempo al siguiente evento: llegada o salida
        t = min(proxima_llegada, proxima_salida)

        # Acumula el área (para obtener promedios al final)
        area_en_sistema += len(cola) * (t - tiempo_ultimo_evento)
        # Si el servidor está ocupado, hay un cliente menos en cola (el que está siendo atendido)
        area_en_cola += (len(cola) - (1 if servidor_ocupado else 0)) * (t - tiempo_ultimo_evento)
        if servidor_ocupado:
            tiempo_ocupado += t - tiempo_ultimo_evento

        tiempo_ultimo_evento = t

        # Si el evento es una llegada
        if t == proxima_llegada:
            # Si hay espacio en la cola, se agrega el cliente
            if len(cola) < tamaño_maximo_cola:
                cola.append(t)  # Guardamos el tiempo de llegada del cliente
                # Si el servidor está libre, se atiende inmediatamente
                if not servidor_ocupado:
                    servidor_ocupado = True
                    proxima_salida = t + np.random.exponential(1 / tasa_servicio)
            else:
                # Si la cola está llena, se rechaza al cliente
                rechazados += 1
            # Se programa la próxima llegada
            proxima_llegada = t + np.random.exponential(1 / tasa_arribo)

        else:  # Si el evento es una salida del sistema
            tiempo_llegada = cola.popleft()  # Se saca al cliente que estaba primero en la cola
            demora = t - tiempo_llegada  # Tiempo total que estuvo en el sistema
            tiempos_en_sistema.append(demora)

            # Si hay más clientes esperando, se programa la siguiente salida
            if len(cola) > 0:
                proxima_salida = t + np.random.exponential(1 / tasa_servicio)
            else:
                # Si no hay nadie esperando, el servidor queda libre
                servidor_ocupado = False
                proxima_salida = np.inf

    # Cálculo de la utilización del servidor (tiempo que estuvo ocupado / tiempo total)
    utilizacion = tiempo_ocupado / tiempo_simulacion


    # Devolvemos las métricas principales como un diccionario
    return {
        "promedio_en_sistema": area_en_sistema / tiempo_simulacion,
        "promedio_en_cola": area_en_cola / tiempo_simulacion,
        "tiempo_promedio_sistema": np.mean(tiempos_en_sistema) if tiempos_en_sistema else 0,
        "tiempo_promedio_cola": (area_en_cola / tiempo_simulacion) / tasa_arribo if tasa_arribo > 0 else 0,
        "utilizacion": utilizacion,
        "probabilidad_rechazo": rechazados / (rechazados + len(tiempos_en_sistema)) if (rechazados + len(tiempos_en_sistema)) > 0 else 0
    }

# Función para correr varios experimentos variando la tasa de arribo
def correr_experimentos(mu=1.0, tiempo_simulacion=1000, K=np.inf, cantidad_corridas=50):
    factores_de_carga = [0.25, 0.5, 0.75, 1.0, 1.25]  # λ / μ
    resultados = {}

    for factor in factores_de_carga:
        lam = factor * mu  # Calculamos λ a partir del factor
        # Ejecutamos varias corridas y guardamos los resultados
        corridas = [simular_mm1(lam, mu, tamaño_maximo_cola=K, tiempo_simulacion=tiempo_simulacion) for _ in range(cantidad_corridas)]
        # Promediamos los resultados obtenidos
        promedio = {clave: np.mean([corrida[clave] for corrida in corridas]) for clave in corridas[0]}
        resultados[factor] = promedio  # Guardamos el resultado bajo el factor correspondiente

    return resultados

# Función para graficar los resultados
def graficar_resultados(resultados,mu,k):
    factores = sorted([float(f) for f in resultados.keys()])  # Asegurarse de que estén ordenados como floats
    metricas = list(resultados[factores[0]].keys())  # Tomamos las métricas disponibles

    if not os.path.exists('graficas'):
        os.makedirs('graficas')  # Crear carpeta si no existe

    for metrica in metricas:
        if metrica == "utilizacion":
            # Para la utilización, graficamos como porcentaje
            valores_y = [resultados[f][metrica] * 100 for f in factores]

        else:
            valores_y = [resultados[f][metrica] for f in factores]

        plt.figure()
        plt.plot(factores, valores_y, marker='o', linestyle='-', color='royalblue')
        plt.xlabel('Carga del Sistema (λ / μ)', fontsize=12)
        plt.ylabel(metrica.replace("_", " ").title(), fontsize=12)
        if k != -1:
            plt.title(f'{metrica.replace("_", " ").title()} (μ={mu}, K={k})', fontsize=14)
        else:
            plt.title(f'{metrica.replace("_", " ").title()} (μ={mu}, K=∞)', fontsize=14)
        plt.xticks(factores)  # Marcar los puntos del eje X con los factores directamente
        plt.grid(True)
        plt.tight_layout()
        if not os.path.exists('graficas/mm1k'):
            os.makedirs('graficas/mm1k')
        # Guardar antes de mostrar para que no se limpie la figura
        plt.savefig(f'graficas/mm1k/{metrica}.png')




# Función principal del script
def main():
    # Parser de argumentos para poder correr el script desde consola con distintos parámetros
    parser = argparse.ArgumentParser(description="Simulación M/M/1 con cola finita o infinita")
    parser.add_argument('--mu', type=float, default=1.0, help="Tasa de servicio μ")
    parser.add_argument('--t', type=int, default=1000, help="Tiempo total de simulación")
    parser.add_argument('--k', type=int, default=-1, help="Tamaño máximo de la cola (-1 para infinito)")
    parser.add_argument('--c', type=int, default=10, help="Cantidad de corridas por experimento")

    args = parser.parse_args()
    # Si k es -1, se interpreta como cola infinita
    K = np.inf if args.k == -1 else args.k

    # Ejecutamos los experimentos y graficamos los resultados
    resultados = correr_experimentos(mu=args.mu, tiempo_simulacion=args.t, K=K, cantidad_corridas=args.c)
    graficar_resultados(resultados, args.mu,args.k)

# Punto de entrada del programa
if __name__ == "__main__":
    main()
#python3 sim-mm1k.py --mu 10 --t 1000 --k 2 --c 10