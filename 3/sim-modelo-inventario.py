import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
from typing import List, Dict, Tuple


def simular_inventario(
    s: int, S: int, demanda_media: float, tiempo_simulacion: int,
    costo_orden: float, costo_mantener: float, costo_faltante: float,
    lead_time: int
) -> Dict[str, float | List[int]]:
    """
    Simula una corrida del modelo de inventario (s, S) con demanda Poisson.
    """
    inventario = S
    orden_pendiente, tiempo_orden = None, None

    costos = {"orden": 0, "mantener": 0, "faltante": 0}
    historial = []

    for t in range(tiempo_simulacion):
        if orden_pendiente is not None and t == tiempo_orden:
            inventario += orden_pendiente
            orden_pendiente, tiempo_orden = None, None

        demanda = np.random.poisson(demanda_media)
        inventario -= demanda

        if inventario < 0:
            costos["faltante"] += abs(inventario) * costo_faltante
            inventario = 0

        costos["mantener"] += inventario * costo_mantener

        if inventario <= s and orden_pendiente is None:
            cantidad = S - inventario
            orden_pendiente = cantidad
            tiempo_orden = t + lead_time
            costos["orden"] += costo_orden

        historial.append(inventario)

    costos["total"] = sum(costos.values())
    costos["historial"] = historial
    return costos


def correr_experimentos(
    s: int, S: int, demanda_media: float, tiempo_simulacion: int,
    costo_orden: float, costo_mantener: float, costo_faltante: float,
    lead_time: int, corridas: int
) -> Tuple[Dict[str, float], List[Dict]]:

    resultados = [
        simular_inventario(s, S, demanda_media, tiempo_simulacion,
                           costo_orden, costo_mantener, costo_faltante, lead_time)
        for _ in range(corridas)
    ]

    promedio = {
        k: np.mean([r[k] for r in resultados]) for k in ["orden", "mantener", "faltante", "total"]
    }

    return promedio, resultados






def graficar_inventario(historial: List[int]):
    plt.figure(figsize=(10, 5))
    plt.plot(historial, color="teal", linewidth=2)
    plt.title("Evolución del Inventario (1ª corrida)")
    plt.xlabel("Período")
    plt.ylabel("Unidades")
    plt.grid(True)
    plt.tight_layout()
    if not os.path.exists("graficas/inventario"):
        os.makedirs("graficas/inventario")
    plt.savefig("graficas/inventario/evolucion_inventario.png")
    plt.close()


def graficar_costos_promedio(promedios: Dict[str, float]):
    categorias = ["orden", "mantener", "faltante"]
    valores = [promedios[c] for c in categorias]

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, valores, color=["orange", "steelblue", "crimson"])
    plt.title("Costo Promedio por Categoría")
    plt.ylabel("Costo")
    plt.tight_layout()
    if not os.path.exists("graficas/costos"):
        os.makedirs("graficas/costos")
    plt.savefig("graficas/costos/costos_promedio.png")
    plt.close()


def graficar_costos_por_corrida(resultados: List[Dict[str, float]]):
    corridas = range(len(resultados))
    for metrica, color in zip(["orden", "mantener", "faltante", "total"],
                              ["darkorange", "royalblue", "firebrick", "forestgreen"]):
        plt.figure(figsize=(10, 4))
        plt.plot(corridas, [r[metrica] for r in resultados], marker="o", color=color)
        plt.title(f"{metrica.capitalize()} por Corrida")
        plt.xlabel("Corrida")
        plt.ylabel("Costo")
        plt.grid(True)
        plt.tight_layout()
        if not os.path.exists("graficas/costos"):
            os.makedirs("graficas/costos")
        plt.savefig(f"graficas/costos/{metrica}_por_corrida.png")
        plt.close()



def main():
    parser = argparse.ArgumentParser(description="Simulación del modelo de inventario (s, S)")

    parser.add_argument("--s", type=int, default=20, help="Punto de reorden (s)")
    parser.add_argument("--S", type=int, default=80, help="Nivel objetivo de inventario (S)")
    parser.add_argument("--d", type=float, default=5.0, help="Demanda media")
    parser.add_argument("--t", type=int, default=100, help="Períodos de simulación")
    parser.add_argument("--co", type=float, default=50.0, help="Costo por orden")
    parser.add_argument("--cm", type=float, default=1.0, help="Costo de mantenimiento")
    parser.add_argument("--cf", type=float, default=10.0, help="Costo por faltante")
    parser.add_argument("--l", type=int, default=2, help="Lead time (períodos)")
    parser.add_argument("--c", type=int, default=10, help="Cantidad de corridas")

    args = parser.parse_args()

    if args.s > args.S:
        raise ValueError("El valor de s no puede ser mayor que S")

    promedio, resultados = correr_experimentos(
        args.s, args.S, args.d, args.t, args.co, args.cm, args.cf, args.l, args.c
    )

    print("RESULTADOS PROMEDIO")
    for clave, valor in promedio.items():
        print(f"  {clave.capitalize():<10}: ${valor:.2f}")

    graficar_inventario(resultados[0]["historial"])
    graficar_costos_promedio(promedio)
    graficar_costos_por_corrida(resultados)


if __name__ == "__main__":
    main()
# python3 sim-modelo-inventario.py --s 20 --S 100 --d 7 --t 365 --co 100 --cm 0.2 --cf 5 --l 3 --c 30
