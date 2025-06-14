import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def simular_inventario(s, S, demanda_media, tiempo_simulacion, costo_orden,
                       costo_mantener, costo_faltante, lead_time):
    """Simula una única corrida del modelo (s, S)."""
    inventario = S  # Inventario inicial
    orden_pendiente, tiempo_orden = None, None  # Pedido en tránsito

    # Acumuladores de costos
    costo_orden_total = 0
    costo_mantener_total = 0
    costo_faltante_total = 0

    historial_inventario = []  # Para graficar

    for t in range(tiempo_simulacion):
        # 1) Comprobar llegada de la orden pendiente
        if orden_pendiente is not None and t == tiempo_orden:
            inventario += orden_pendiente
            orden_pendiente, tiempo_orden = None, None

        # 2) Generar demanda de este período (Poisson)
        demanda = np.random.poisson(demanda_media)
        inventario -= demanda

        # 3) Costos de faltantes, si la demanda > inventario
        if inventario < 0:
            costo_faltante_total += abs(inventario) * costo_faltante
            inventario = 0  # No permitimos inventario negativo

        # 4) Costos de mantenimiento por inventario remanente
        costo_mantener_total += inventario * costo_mantener

        # 5) Política de reposición (s, S)
        if inventario <= s and orden_pendiente is None:
            cantidad_a_ordenar = S - inventario
            orden_pendiente = cantidad_a_ordenar
            tiempo_orden = t + lead_time
            costo_orden_total += costo_orden

        # Guardar estado para la gráfica
        historial_inventario.append(inventario)

    # 6) Coste total de la corrida
    costo_total = costo_orden_total + costo_mantener_total + costo_faltante_total

    return {
        "orden": costo_orden_total,
        "mantener": costo_mantener_total,
        "faltante": costo_faltante_total,
        "total": costo_total,
        "historial": historial_inventario,
    }


def correr_experimentos(s, S, demanda_media, tiempo_simulacion, costo_orden,
                        costo_mantener, costo_faltante, lead_time, corridas):
    """Ejecuta varias corridas y devuelve promedios + lista completa."""
    resultados = [
        simular_inventario(s, S, demanda_media, tiempo_simulacion, costo_orden,
                           costo_mantener, costo_faltante, lead_time)
        for _ in range(corridas)
    ]

    promedio = {
        k: np.mean([r[k] for r in resultados]) for k in ["orden", "mantener", "faltante", "total"]
    }
    return promedio, resultados

# ---------- FUNCIONES DE GRÁFICA ----------

def _asegurar_carpeta(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def graficar_inventario(resultados):
    """Gráfica la evolución del inventario de la PRIMERA corrida."""
    _asegurar_carpeta("graficas/inventario")
    plt.figure(figsize=(10, 5))
    plt.plot(resultados[0]["historial"], color="teal")
    plt.title("Evolución del Inventario (1ª corrida)")
    plt.xlabel("Período")
    plt.ylabel("Unidades en inventario")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/inventario/evolucion_inventario.png")
    plt.close()


def graficar_costos_promedio(promedio):
    """Bar chart con el costo promedio de cada categoría."""
    _asegurar_carpeta("graficas/costos")
    categorias = ["orden", "mantener", "faltante"]
    valores = [promedio[c] for c in categorias]

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, valores, color=["orange", "steelblue", "crimson"])
    plt.ylabel("Costo promedio")
    plt.title("Costos promedio por categoría")
    plt.tight_layout()
    if not os.path.exists("graficas/inventario"):
        os.makedirs("graficas/inventario")
    plt.savefig("graficas/inventario/costos_promedio.png")
    plt.close()


def graficar_costos_corridas(resultados):
    """Line chart para comparar los costos de cada corrida."""
    _asegurar_carpeta("graficas/inventario")
    corridas = range(len(resultados))
    for metrica, color in zip(["orden", "mantener", "faltante", "total"],
                              ["darkorange", "royalblue", "firebrick", "forestgreen"]):
        plt.figure(figsize=(10, 4))
        plt.plot(corridas, [r[metrica] for r in resultados], marker="o", color=color)
        plt.title(f"{metrica.capitalize()} por corrida")
        plt.xlabel("Corrida")
        plt.ylabel("Costo")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"graficas/inventario/{metrica}_por_corrida.png")
        plt.close()

# ---------- MAIN ----------

def main():
    parser = argparse.ArgumentParser(description="Simulación de Inventario (s, S)")
    parser.add_argument("--s", type=int, default=20, help="Punto de reorden (s)")
    parser.add_argument("--S", type=int, default=80, help="Nivel máximo de inventario (S)")
    parser.add_argument("--d", type=float, default=5.0, help="Demanda media (Poisson)")
    parser.add_argument("--t", type=int, default=100, help="Tiempo de simulación (períodos)")
    parser.add_argument("--co", type=float, default=50.0, help="Costo de orden")
    parser.add_argument("--cm", type=float, default=1.0, help="Costo de mantenimiento por unidad")
    parser.add_argument("--cf", type=float, default=10.0, help="Costo por faltante")
    parser.add_argument("--l", type=int, default=2, help="Lead time")
    parser.add_argument("--c", type=int, default=10, help="Número de corridas")

    args = parser.parse_args()

    promedio, resultados = correr_experimentos(
        s=args.s,
        S=args.S,
        demanda_media=args.d,
        tiempo_simulacion=args.t,
        costo_orden=args.co,
        costo_mantener=args.cm,
        costo_faltante=args.cf,
        lead_time=args.l,
        corridas=args.c,
    )

    # Mostrar resultados en consola
    print("\n--- Resultados Promediados ---")
    print(f"Costo de orden: ${promedio['orden']:.2f}")
    print(f"Costo de mantenimiento: ${promedio['mantener']:.2f}")
    print(f"Costo por faltantes: ${promedio['faltante']:.2f}")
    print(f"Costo total: ${promedio['total']:.2f}")

    # Generar todas las gráficas
    graficar_inventario(resultados)
    graficar_costos_promedio(promedio)
    graficar_costos_corridas(resultados)


if __name__ == "__main__":
    main()


# python3 sim-modelo-inventario.py --s 10 --S 100 --d 10 --t 1000 --co 30 --cm 4 --cf 20 --l 10 --c 10