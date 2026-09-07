from pathlib import Path
import csv
import html
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1]
SALIDA_DIR = BASE_DIR / "salida_resultados"
GRAFICOS_DIR = SALIDA_DIR / "graficos"
RESUMEN_CSV = SALIDA_DIR / "resumen_resultados.csv"
DASHBOARD_HTML = SALIDA_DIR / "dashboard_resultados.html"

COLORES = {
    "BFS": "#2563eb",
    "DFS": "#f97316",
}

METRICAS = [
    {
        "campo": "promTiempo",
        "titulo": "Tiempo promedio por escenario",
        "subtitulo": "Menor valor significa menor tiempo de ejecucion.",
        "archivo": "tiempo_promedio.svg",
        "unidad": " ms",
        "decimales": 3,
    },
    {
        "campo": "promVisitados",
        "titulo": "Nodos visitados promedio",
        "subtitulo": "Mide cuanto explora cada algoritmo antes de llegar al destino.",
        "archivo": "nodos_visitados.svg",
        "unidad": " nodos",
        "decimales": 1,
    },
    {
        "campo": "promRuta",
        "titulo": "Longitud promedio de la ruta",
        "subtitulo": "En grafos no ponderados, BFS suele encontrar rutas con menos tramos.",
        "archivo": "longitud_ruta.svg",
        "unidad": " tramos",
        "decimales": 1,
    },
    {
        "campo": "promMemoria",
        "titulo": "Memoria aproximada promedio",
        "subtitulo": "Se estima con nodos visitados mas el maximo de cola o pila.",
        "archivo": "memoria_aproximada.svg",
        "unidad": " unidades",
        "decimales": 1,
    },
]


def leer_resumen():
    if not RESUMEN_CSV.exists():
        raise SystemExit(
            "No existe salida_resultados/resumen_resultados.csv. "
            "Primero ejecuta la opcion 2 del programa Java."
        )

    filas = []
    with RESUMEN_CSV.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")
        for fila in lector:
            obstaculos = fila["obstaculos"].replace("%", "")
            filas.append(
                {
                    "tamano": int(fila["tamano"]),
                    "obstaculos": int(obstaculos),
                    "algoritmo": fila["algoritmo"],
                    "promTiempo": float(fila["promTiempo"]),
                    "medianaTiempo": float(fila["medianaTiempo"]),
                    "desvTiempo": float(fila["desvTiempo"]),
                    "promVisitados": float(fila["promVisitados"]),
                    "promRuta": float(fila["promRuta"]),
                    "promMemoria": float(fila["promMemoria"]),
                }
            )
    return filas


def escenarios_ordenados(filas):
    vistos = []
    for fila in filas:
        clave = (fila["tamano"], fila["obstaculos"])
        if clave not in vistos:
            vistos.append(clave)
    return sorted(vistos)


def buscar_fila(filas, tamano, obstaculos, algoritmo):
    for fila in filas:
        if (
            fila["tamano"] == tamano
            and fila["obstaculos"] == obstaculos
            and fila["algoritmo"] == algoritmo
        ):
            return fila
    return None


def formato_numero(valor, decimales):
    return f"{valor:.{decimales}f}"


def svg_texto(x, y, texto, clase="", anchor="middle", extra=""):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{clase}" {extra}>'
        f"{html.escape(str(texto))}</text>"
    )


def generar_svg_barras(filas, metrica):
    escenarios = escenarios_ordenados(filas)
    valores = []
    for tamano, obstaculos in escenarios:
        for algoritmo in ("BFS", "DFS"):
            fila = buscar_fila(filas, tamano, obstaculos, algoritmo)
            if fila:
                valores.append(fila[metrica["campo"]])

    maximo = max(valores) if valores else 1
    if maximo <= 0:
        maximo = 1

    ancho = 1120
    alto = 540
    margen_izq = 76
    margen_der = 32
    margen_sup = 92
    margen_inf = 112
    graf_ancho = ancho - margen_izq - margen_der
    graf_alto = alto - margen_sup - margen_inf
    grupo_ancho = graf_ancho / len(escenarios)
    barra_ancho = min(28, grupo_ancho * 0.28)
    escala_max = maximo * 1.15

    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        "<style>",
        ".titulo{font:700 24px Arial, sans-serif;fill:#111827}",
        ".subtitulo{font:400 14px Arial, sans-serif;fill:#4b5563}",
        ".eje{font:400 12px Arial, sans-serif;fill:#374151}",
        ".valor{font:700 11px Arial, sans-serif;fill:#111827}",
        ".leyenda{font:700 13px Arial, sans-serif;fill:#111827}",
        ".grid{stroke:#e5e7eb;stroke-width:1}",
        ".axis{stroke:#9ca3af;stroke-width:1.3}",
        "</style>",
        '<rect x="0" y="0" width="1120" height="540" rx="0" fill="#ffffff"/>',
        svg_texto(ancho / 2, 34, metrica["titulo"], "titulo"),
        svg_texto(ancho / 2, 58, metrica["subtitulo"], "subtitulo"),
    ]

    for i in range(6):
        valor_tick = escala_max * i / 5
        y = margen_sup + graf_alto - (valor_tick / escala_max) * graf_alto
        partes.append(f'<line x1="{margen_izq}" y1="{y:.1f}" x2="{ancho - margen_der}" y2="{y:.1f}" class="grid"/>')
        partes.append(svg_texto(64, y + 4, formato_numero(valor_tick, metrica["decimales"]), "eje", "end"))

    partes.append(f'<line x1="{margen_izq}" y1="{margen_sup}" x2="{margen_izq}" y2="{margen_sup + graf_alto}" class="axis"/>')
    partes.append(f'<line x1="{margen_izq}" y1="{margen_sup + graf_alto}" x2="{ancho - margen_der}" y2="{margen_sup + graf_alto}" class="axis"/>')

    leyenda_x = ancho - 190
    leyenda_y = 78
    partes.append(f'<rect x="{leyenda_x}" y="{leyenda_y - 13}" width="14" height="14" fill="{COLORES["BFS"]}"/>')
    partes.append(svg_texto(leyenda_x + 22, leyenda_y, "BFS", "leyenda", "start"))
    partes.append(f'<rect x="{leyenda_x + 70}" y="{leyenda_y - 13}" width="14" height="14" fill="{COLORES["DFS"]}"/>')
    partes.append(svg_texto(leyenda_x + 92, leyenda_y, "DFS", "leyenda", "start"))

    for indice, (tamano, obstaculos) in enumerate(escenarios):
        centro = margen_izq + grupo_ancho * indice + grupo_ancho / 2
        etiqueta_1 = f"{tamano}x{tamano}"
        etiqueta_2 = f"{obstaculos}% obs."

        for pos, algoritmo in enumerate(("BFS", "DFS")):
            fila = buscar_fila(filas, tamano, obstaculos, algoritmo)
            if not fila:
                continue

            valor = fila[metrica["campo"]]
            barra_alto = (valor / escala_max) * graf_alto
            x = centro - barra_ancho - 3 if pos == 0 else centro + 3
            y = margen_sup + graf_alto - barra_alto
            color = COLORES[algoritmo]

            partes.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{barra_ancho:.1f}" '
                f'height="{barra_alto:.1f}" fill="{color}"/>'
            )
            partes.append(
                svg_texto(
                    x + barra_ancho / 2,
                    max(y - 6, margen_sup - 8),
                    formato_numero(valor, metrica["decimales"]),
                    "valor",
                )
            )

        partes.append(svg_texto(centro, margen_sup + graf_alto + 26, etiqueta_1, "eje"))
        partes.append(svg_texto(centro, margen_sup + graf_alto + 44, etiqueta_2, "eje"))

    partes.append("</svg>")
    return "\n".join(partes)


def tabla_html(filas):
    orden = escenarios_ordenados(filas)
    lineas = [
        "<table>",
        "<thead>",
        "<tr><th>Escenario</th><th>Algoritmo</th><th>Tiempo prom.</th><th>Nodos prom.</th><th>Ruta prom.</th><th>Memoria prom.</th></tr>",
        "</thead>",
        "<tbody>",
    ]
    for tamano, obstaculos in orden:
        for algoritmo in ("BFS", "DFS"):
            fila = buscar_fila(filas, tamano, obstaculos, algoritmo)
            if not fila:
                continue
            lineas.append(
                "<tr>"
                f"<td>{tamano}x{tamano} - {obstaculos}%</td>"
                f"<td><span class='pill {algoritmo.lower()}'>{algoritmo}</span></td>"
                f"<td>{fila['promTiempo']:.4f} ms</td>"
                f"<td>{fila['promVisitados']:.1f}</td>"
                f"<td>{fila['promRuta']:.1f}</td>"
                f"<td>{fila['promMemoria']:.1f}</td>"
                "</tr>"
            )
    lineas.extend(["</tbody>", "</table>"])
    return "\n".join(lineas)


def resumen_rapido(filas):
    escenarios = escenarios_ordenados(filas)
    bfs_menor_ruta = 0
    dfs_menor_tiempo = 0
    dfs_menos_visitados = 0

    for tamano, obstaculos in escenarios:
        bfs = buscar_fila(filas, tamano, obstaculos, "BFS")
        dfs = buscar_fila(filas, tamano, obstaculos, "DFS")
        if not bfs or not dfs:
            continue
        if bfs["promRuta"] <= dfs["promRuta"]:
            bfs_menor_ruta += 1
        if dfs["promTiempo"] < bfs["promTiempo"]:
            dfs_menor_tiempo += 1
        if dfs["promVisitados"] < bfs["promVisitados"]:
            dfs_menos_visitados += 1

    return {
        "escenarios": len(escenarios),
        "bfs_menor_ruta": bfs_menor_ruta,
        "dfs_menor_tiempo": dfs_menor_tiempo,
        "dfs_menos_visitados": dfs_menos_visitados,
    }


def generar_dashboard(filas, archivos_svg):
    resumen = resumen_rapido(filas)
    generado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tarjetas = [
        ("Escenarios evaluados", str(resumen["escenarios"])),
        ("BFS con ruta igual o menor", f"{resumen['bfs_menor_ruta']} de {resumen['escenarios']}"),
        ("DFS con menor tiempo", f"{resumen['dfs_menor_tiempo']} de {resumen['escenarios']}"),
        ("DFS con menos nodos visitados", f"{resumen['dfs_menos_visitados']} de {resumen['escenarios']}"),
    ]

    tarjetas_html = "\n".join(
        f"<section class='card'><p>{html.escape(titulo)}</p><strong>{html.escape(valor)}</strong></section>"
        for titulo, valor in tarjetas
    )

    graficos_html = "\n".join(
        "<section class='chart'>"
        f"<img src='graficos/{html.escape(archivo)}' alt='{html.escape(archivo)}'>"
        "</section>"
        for archivo in archivos_svg
    )

    contenido = f"""<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard BFS vs DFS</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f3f4f6;
            --panel: #ffffff;
            --text: #111827;
            --muted: #4b5563;
            --line: #d1d5db;
            --bfs: #2563eb;
            --dfs: #f97316;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
        }}
        header {{
            background: #111827;
            color: white;
            padding: 28px 36px;
        }}
        header h1 {{
            margin: 0 0 8px;
            font-size: 30px;
        }}
        header p {{
            margin: 0;
            color: #d1d5db;
        }}
        main {{
            width: min(1180px, calc(100% - 32px));
            margin: 24px auto 48px;
        }}
        .cards {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-bottom: 20px;
        }}
        .card {{
            background: var(--panel);
            border: 1px solid var(--line);
            padding: 16px;
        }}
        .card p {{
            margin: 0 0 8px;
            color: var(--muted);
            font-size: 13px;
        }}
        .card strong {{
            font-size: 24px;
        }}
        .chart {{
            background: var(--panel);
            border: 1px solid var(--line);
            margin-bottom: 18px;
            padding: 12px;
            overflow-x: auto;
        }}
        .chart img {{
            width: 100%;
            min-width: 860px;
            display: block;
        }}
        .table-wrap {{
            background: var(--panel);
            border: 1px solid var(--line);
            padding: 16px;
            overflow-x: auto;
        }}
        h2 {{
            margin: 4px 0 16px;
            font-size: 22px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            font-size: 14px;
        }}
        th, td {{
            border-bottom: 1px solid #e5e7eb;
            padding: 10px;
            text-align: left;
            white-space: nowrap;
        }}
        th {{
            background: #f9fafb;
            color: #374151;
        }}
        .pill {{
            color: white;
            padding: 3px 9px;
            font-weight: 700;
            font-size: 12px;
        }}
        .pill.bfs {{ background: var(--bfs); }}
        .pill.dfs {{ background: var(--dfs); }}
        footer {{
            color: var(--muted);
            font-size: 13px;
            margin-top: 18px;
        }}
        @media (max-width: 850px) {{
            .cards {{ grid-template-columns: repeat(2, 1fr); }}
            header {{ padding: 22px 20px; }}
        }}
        @media (max-width: 520px) {{
            .cards {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Comparacion BFS vs DFS</h1>
        <p>Graficos generados desde salida_resultados/resumen_resultados.csv</p>
    </header>
    <main>
        <section class="cards">
            {tarjetas_html}
        </section>
        {graficos_html}
        <section class="table-wrap">
            <h2>Tabla resumen</h2>
            {tabla_html(filas)}
        </section>
        <footer>
            Generado: {html.escape(generado)}. Archivos individuales SVG guardados en salida_resultados/graficos.
        </footer>
    </main>
</body>
</html>
"""
    DASHBOARD_HTML.write_text(contenido, encoding="utf-8")


def main():
    filas = leer_resumen()
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    archivos_svg = []
    for metrica in METRICAS:
        svg = generar_svg_barras(filas, metrica)
        destino = GRAFICOS_DIR / metrica["archivo"]
        destino.write_text(svg, encoding="utf-8")
        archivos_svg.append(metrica["archivo"])

    generar_dashboard(filas, archivos_svg)
    print("Graficos generados correctamente.")
    print(f"- {DASHBOARD_HTML}")
    for archivo in archivos_svg:
        print(f"- {GRAFICOS_DIR / archivo}")


if __name__ == "__main__":
    main()
