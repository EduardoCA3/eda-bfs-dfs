from pathlib import Path
import csv
import html
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]
SALIDA_DIR = BASE_DIR / "salida_resultados"
GRAFICOS_DIR = SALIDA_DIR / "graficos"
CSV_PRUEBA = SALIDA_DIR / "prueba_simple_resultados.csv"
DASHBOARD_HTML = SALIDA_DIR / "dashboard_prueba_simple.html"

COLORES = {
    "BFS": "#2563eb",
    "DFS": "#f97316",
}

METRICAS = [
    ("tiempoMs", "Tiempo de ejecucion", "ms", 4),
    ("nodosVisitados", "Nodos visitados", "nodos", 0),
    ("longitudRuta", "Longitud de ruta", "tramos", 0),
    ("memoriaAprox", "Memoria aproximada", "unidades", 0),
]


def leer_csv():
    if not CSV_PRUEBA.exists():
        raise SystemExit(
            "No existe salida_resultados/prueba_simple_resultados.csv. "
            "Primero ejecuta la opcion 1 del programa Java."
        )

    filas = []
    with CSV_PRUEBA.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for fila in lector:
            filas.append(
                {
                    "algoritmo": fila["algoritmo"],
                    "tiempoMs": float(fila["tiempoMs"]),
                    "nodosVisitados": float(fila["nodosVisitados"]),
                    "longitudRuta": float(fila["longitudRuta"]),
                    "maxColaPila": float(fila["maxColaPila"]),
                    "memoriaAprox": float(fila["memoriaAprox"]),
                }
            )
    return filas


def fmt(valor, decimales):
    if decimales == 0:
        return str(int(round(valor)))
    return f"{valor:.{decimales}f}"


def svg_texto(x, y, texto, clase="", anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{clase}">'
        f"{html.escape(str(texto))}</text>"
    )


def generar_svg(filas, campo, titulo, unidad, decimales):
    ancho = 620
    alto = 360
    margen_izq = 70
    margen_inf = 70
    margen_sup = 72
    margen_der = 30
    graf_ancho = ancho - margen_izq - margen_der
    graf_alto = alto - margen_sup - margen_inf
    maximo = max(fila[campo] for fila in filas) * 1.2
    if maximo <= 0:
        maximo = 1

    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        "<style>",
        ".titulo{font:700 22px Arial,sans-serif;fill:#111827}",
        ".eje{font:400 12px Arial,sans-serif;fill:#4b5563}",
        ".valor{font:700 13px Arial,sans-serif;fill:#111827}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#9ca3af;stroke-width:1.2}",
        "</style>",
        '<rect x="0" y="0" width="620" height="360" fill="#ffffff"/>',
        svg_texto(ancho / 2, 32, titulo, "titulo"),
        svg_texto(ancho / 2, 54, f"Prueba simple 10x10 - valores en {unidad}", "eje"),
    ]

    for i in range(5):
        valor_tick = maximo * i / 4
        y = margen_sup + graf_alto - (valor_tick / maximo) * graf_alto
        partes.append(f'<line x1="{margen_izq}" y1="{y:.1f}" x2="{ancho - margen_der}" y2="{y:.1f}" class="grid"/>')
        partes.append(svg_texto(58, y + 4, fmt(valor_tick, decimales), "eje", "end"))

    partes.append(f'<line x1="{margen_izq}" y1="{margen_sup}" x2="{margen_izq}" y2="{margen_sup + graf_alto}" class="axis"/>')
    partes.append(f'<line x1="{margen_izq}" y1="{margen_sup + graf_alto}" x2="{ancho - margen_der}" y2="{margen_sup + graf_alto}" class="axis"/>')

    barra_ancho = 90
    centros = [margen_izq + graf_ancho * 0.32, margen_izq + graf_ancho * 0.68]

    for indice, fila in enumerate(filas):
        algoritmo = fila["algoritmo"]
        valor = fila[campo]
        barra_alto = (valor / maximo) * graf_alto
        x = centros[indice] - barra_ancho / 2
        y = margen_sup + graf_alto - barra_alto
        partes.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{barra_ancho}" '
            f'height="{barra_alto:.1f}" fill="{COLORES.get(algoritmo, "#6b7280")}"/>'
        )
        partes.append(svg_texto(centros[indice], max(y - 8, 68), fmt(valor, decimales), "valor"))
        partes.append(svg_texto(centros[indice], margen_sup + graf_alto + 28, algoritmo, "eje"))

    partes.append("</svg>")
    return "\n".join(partes)


def tabla_html(filas):
    lineas = [
        "<table>",
        "<thead><tr><th>Algoritmo</th><th>Tiempo</th><th>Nodos visitados</th><th>Ruta</th><th>Max cola/pila</th><th>Memoria</th></tr></thead>",
        "<tbody>",
    ]
    for fila in filas:
        algoritmo = html.escape(fila["algoritmo"])
        lineas.append(
            "<tr>"
            f"<td><span class='pill {algoritmo.lower()}'>{algoritmo}</span></td>"
            f"<td>{fila['tiempoMs']:.4f} ms</td>"
            f"<td>{int(fila['nodosVisitados'])}</td>"
            f"<td>{int(fila['longitudRuta'])}</td>"
            f"<td>{int(fila['maxColaPila'])}</td>"
            f"<td>{int(fila['memoriaAprox'])}</td>"
            "</tr>"
        )
    lineas.extend(["</tbody>", "</table>"])
    return "\n".join(lineas)


def generar_dashboard(filas, archivos):
    generado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    imagenes = "\n".join(
        f"<section class='chart'><img src='graficos/{html.escape(archivo)}' alt='{html.escape(archivo)}'></section>"
        for archivo in archivos
    )

    contenido = f"""<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Grafico prueba simple BFS vs DFS</title>
    <style>
        body {{ margin: 0; font-family: Arial, sans-serif; background: #f3f4f6; color: #111827; }}
        header {{ background: #111827; color: white; padding: 26px 34px; }}
        header h1 {{ margin: 0 0 8px; font-size: 30px; }}
        header p {{ margin: 0; color: #d1d5db; }}
        main {{ width: min(1120px, calc(100% - 32px)); margin: 22px auto 44px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
        .chart, .table-wrap {{ background: white; border: 1px solid #d1d5db; padding: 12px; overflow-x: auto; }}
        .chart img {{ width: 100%; min-width: 520px; display: block; }}
        .table-wrap {{ margin-top: 18px; padding: 16px; }}
        table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
        th, td {{ border-bottom: 1px solid #e5e7eb; padding: 10px; text-align: left; white-space: nowrap; }}
        th {{ background: #f9fafb; color: #374151; }}
        .pill {{ color: white; padding: 3px 9px; font-weight: 700; font-size: 12px; }}
        .pill.bfs {{ background: #2563eb; }}
        .pill.dfs {{ background: #f97316; }}
        footer {{ color: #4b5563; margin-top: 16px; font-size: 13px; }}
        @media (max-width: 850px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <h1>Prueba simple BFS vs DFS</h1>
        <p>Graficos de barras generados desde salida_resultados/prueba_simple_resultados.csv</p>
    </header>
    <main>
        <section class="grid">
            {imagenes}
        </section>
        <section class="table-wrap">
            <h2>Datos usados</h2>
            {tabla_html(filas)}
        </section>
        <footer>Generado: {html.escape(generado)}</footer>
    </main>
</body>
</html>
"""
    DASHBOARD_HTML.write_text(contenido, encoding="utf-8")


def main():
    filas = leer_csv()
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    archivos = []

    for campo, titulo, unidad, decimales in METRICAS:
        archivo = f"prueba_simple_{campo}.svg"
        (GRAFICOS_DIR / archivo).write_text(
            generar_svg(filas, campo, titulo, unidad, decimales),
            encoding="utf-8",
        )
        archivos.append(archivo)

    generar_dashboard(filas, archivos)
    print("Grafico de prueba simple generado correctamente.")
    print(f"- {DASHBOARD_HTML}")


if __name__ == "__main__":
    main()
