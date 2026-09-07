from pathlib import Path
import json
import html


BASE_DIR = Path(__file__).resolve().parents[1]
SALIDA_DIR = BASE_DIR / "salida_resultados"
MAPA_TXT = SALIDA_DIR / "mapa_ejemplo.txt"
ANIMACION_HTML = SALIDA_DIR / "animacion_grafos.html"

DIRECCIONES = [
    ("arriba", -1, 0),
    ("derecha", 0, 1),
    ("abajo", 1, 0),
    ("izquierda", 0, -1),
]


def leer_mapa():
    if not MAPA_TXT.exists():
        raise SystemExit(
            "No existe salida_resultados/mapa_ejemplo.txt. "
            "Primero ejecuta la opcion 1 del programa Java."
        )

    filas = []
    leyendo_mapa = False
    with MAPA_TXT.open("r", encoding="utf-8-sig") as archivo:
        for linea in archivo:
            texto = linea.strip()
            if not texto:
                if leyendo_mapa and filas:
                    break
                continue
            if texto.startswith("S = inicio"):
                leyendo_mapa = True
                continue
            if leyendo_mapa:
                tokens = texto.split()
                if tokens and all(token in {"S", "G", "#", "."} for token in tokens):
                    filas.append(tokens)

    if not filas:
        raise SystemExit("No se pudo leer el mapa dentro de salida_resultados/mapa_ejemplo.txt.")

    mapa = []
    inicio = None
    destino = None
    for fila, tokens in enumerate(filas):
        mapa.append([])
        for columna, token in enumerate(tokens):
            if token == "#":
                mapa[fila].append(1)
            else:
                mapa[fila].append(0)
            if token == "S":
                inicio = (fila, columna)
            elif token == "G":
                destino = (fila, columna)

    if inicio is None:
        inicio = (0, 0)
    if destino is None:
        destino = (len(mapa) - 1, len(mapa[0]) - 1)

    return mapa, inicio, destino


def id_pos(posicion):
    return f"{posicion[0]}-{posicion[1]}"


def dentro(mapa, fila, columna):
    return 0 <= fila < len(mapa) and 0 <= columna < len(mapa[0])


def libre(mapa, fila, columna):
    return dentro(mapa, fila, columna) and mapa[fila][columna] == 0


def reconstruir_ruta(padres, inicio, destino):
    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        if actual == inicio:
            break
        actual = padres.get(actual)
    if not ruta or ruta[-1] != inicio:
        return []
    ruta.reverse()
    return ruta


def crear_frame(paso, titulo, descripcion, estructura, descubiertos, procesados, actual, ruta=None):
    return {
        "paso": paso,
        "titulo": titulo,
        "descripcion": descripcion,
        "estructura": [list(pos) for pos in estructura],
        "descubiertos": [list(pos) for pos in sorted(descubiertos)],
        "procesados": [list(pos) for pos in sorted(procesados)],
        "actual": list(actual) if actual is not None else None,
        "ruta": [list(pos) for pos in ruta] if ruta else [],
    }


def simular_bfs(mapa, inicio, destino):
    cola = [inicio]
    descubiertos = {inicio}
    procesados = set()
    padres = {}
    frames = [
        crear_frame(
            0,
            "Inicio BFS",
            "Se coloca el nodo inicial en la cola. BFS explora por niveles.",
            cola,
            descubiertos,
            procesados,
            None,
        )
    ]

    paso = 1
    while cola:
        actual = cola.pop(0)
        procesados.add(actual)

        if actual == destino:
            ruta = reconstruir_ruta(padres, inicio, destino)
            frames.append(
                crear_frame(
                    paso,
                    "BFS encontro el destino",
                    "El destino salio de la cola. Se reconstruye la ruta usando los padres.",
                    cola,
                    descubiertos,
                    procesados,
                    actual,
                    ruta,
                )
            )
            return frames, ruta

        cambios = []
        for nombre, df, dc in DIRECCIONES:
            nueva = (actual[0] + df, actual[1] + dc)
            if libre(mapa, nueva[0], nueva[1]) and nueva not in descubiertos:
                descubiertos.add(nueva)
                padres[nueva] = actual
                cola.append(nueva)
                cambios.append(f"{nombre}: agrega ({nueva[0]},{nueva[1]})")

        if cambios:
            descripcion = "Procesa ({},{}). ".format(actual[0], actual[1]) + "; ".join(cambios) + "."
        else:
            descripcion = "Procesa ({},{}). No agrega nuevos vecinos.".format(actual[0], actual[1])

        frames.append(
            crear_frame(
                paso,
                "Paso BFS",
                descripcion,
                cola,
                descubiertos,
                procesados,
                actual,
            )
        )
        paso += 1

    return frames, []


def simular_dfs(mapa, inicio, destino):
    pila = [inicio]
    descubiertos = {inicio}
    procesados = set()
    padres = {}
    frames = [
        crear_frame(
            0,
            "Inicio DFS",
            "Se coloca el nodo inicial en la pila. DFS avanza en profundidad.",
            pila,
            descubiertos,
            procesados,
            None,
        )
    ]

    paso = 1
    while pila:
        actual = pila.pop()
        if actual in procesados:
            continue

        procesados.add(actual)

        if actual == destino:
            ruta = reconstruir_ruta(padres, inicio, destino)
            frames.append(
                crear_frame(
                    paso,
                    "DFS encontro el destino",
                    "El destino salio de la pila. Se reconstruye la ruta usando los padres.",
                    pila,
                    descubiertos,
                    procesados,
                    actual,
                    ruta,
                )
            )
            return frames, ruta

        cambios = []
        for nombre, df, dc in reversed(DIRECCIONES):
            nueva = (actual[0] + df, actual[1] + dc)
            if libre(mapa, nueva[0], nueva[1]) and nueva not in descubiertos:
                descubiertos.add(nueva)
                padres[nueva] = actual
                pila.append(nueva)
                cambios.append(f"{nombre}: apila ({nueva[0]},{nueva[1]})")

        if cambios:
            descripcion = "Procesa ({},{}). ".format(actual[0], actual[1]) + "; ".join(cambios) + "."
        else:
            descripcion = "Procesa ({},{}). No apila nuevos vecinos.".format(actual[0], actual[1])

        frames.append(
            crear_frame(
                paso,
                "Paso DFS",
                descripcion,
                pila,
                descubiertos,
                procesados,
                actual,
            )
        )
        paso += 1

    return frames, []


def generar_html(mapa, inicio, destino, frames_bfs, frames_dfs, ruta_bfs, ruta_dfs):
    datos = {
        "mapa": mapa,
        "inicio": list(inicio),
        "destino": list(destino),
        "bfs": frames_bfs,
        "dfs": frames_dfs,
        "rutaBfs": [list(pos) for pos in ruta_bfs],
        "rutaDfs": [list(pos) for pos in ruta_dfs],
    }

    contenido = f"""<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Animacion BFS y DFS</title>
    <style>
        :root {{
            --bg: #f4f5f7;
            --panel: #ffffff;
            --text: #111827;
            --muted: #4b5563;
            --line: #d1d5db;
            --free: #ffffff;
            --wall: #1f2937;
            --discovered: #fde68a;
            --processed-bfs: #93c5fd;
            --processed-dfs: #fdba74;
            --current: #ef4444;
            --path: #22c55e;
            --start: #16a34a;
            --goal: #7c3aed;
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
            color: #ffffff;
            padding: 24px 32px;
        }}
        h1 {{
            margin: 0 0 8px;
            font-size: 30px;
        }}
        header p {{
            margin: 0;
            color: #d1d5db;
        }}
        main {{
            width: min(1240px, calc(100% - 32px));
            margin: 22px auto 42px;
        }}
        .controls {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            background: var(--panel);
            border: 1px solid var(--line);
            padding: 14px;
            margin-bottom: 16px;
        }}
        button {{
            border: 1px solid #9ca3af;
            background: #ffffff;
            color: #111827;
            font-weight: 700;
            padding: 8px 12px;
            cursor: pointer;
        }}
        button.primary {{
            background: #111827;
            color: #ffffff;
            border-color: #111827;
        }}
        input[type="range"] {{
            flex: 1;
            min-width: 220px;
        }}
        .step-label {{
            min-width: 150px;
            color: var(--muted);
            font-weight: 700;
        }}
        .legend {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            color: var(--muted);
            font-size: 13px;
            margin: 10px 0 18px;
        }}
        .legend span {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
        .swatch {{
            width: 15px;
            height: 15px;
            border: 1px solid #9ca3af;
            display: inline-block;
        }}
        .compare {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        .panel {{
            background: var(--panel);
            border: 1px solid var(--line);
            padding: 16px;
            min-width: 0;
        }}
        .panel h2 {{
            margin: 0 0 8px;
            font-size: 24px;
        }}
        .desc {{
            min-height: 48px;
            color: var(--muted);
            margin: 0 0 14px;
            line-height: 1.35;
        }}
        .grid-wrap {{
            overflow-x: auto;
            padding-bottom: 4px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(var(--cols), 36px);
            grid-auto-rows: 36px;
            gap: 3px;
            width: max-content;
        }}
        .cell {{
            width: 36px;
            height: 36px;
            display: grid;
            place-items: center;
            border: 1px solid #cbd5e1;
            font-size: 11px;
            font-weight: 700;
            color: #111827;
            background: var(--free);
        }}
        .wall {{ background: var(--wall); color: white; border-color: var(--wall); }}
        .discovered {{ background: var(--discovered); }}
        .processed.bfs {{ background: var(--processed-bfs); }}
        .processed.dfs {{ background: var(--processed-dfs); }}
        .path {{ background: var(--path); color: #052e16; border-color: #15803d; }}
        .current {{ background: var(--current); color: white; border-color: #b91c1c; }}
        .start {{ background: var(--start); color: white; border-color: #15803d; }}
        .goal {{ background: var(--goal); color: white; border-color: #6d28d9; }}
        .structure {{
            margin-top: 12px;
            color: var(--muted);
            font-size: 13px;
            line-height: 1.35;
            min-height: 38px;
        }}
        footer {{
            color: var(--muted);
            font-size: 13px;
            margin-top: 18px;
        }}
        @media (max-width: 900px) {{
            .compare {{ grid-template-columns: 1fr; }}
            header {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Animacion del recorrido BFS y DFS</h1>
        <p>Ambos algoritmos recorren el mismo mapa. La diferencia se ve en el orden de exploracion.</p>
    </header>
    <main>
        <section class="controls">
            <button id="prev">Anterior</button>
            <button id="play" class="primary">Reproducir</button>
            <button id="next">Siguiente</button>
            <input id="step" type="range" min="0" value="0">
            <span id="stepLabel" class="step-label">Paso 0</span>
        </section>
        <section class="legend">
            <span><i class="swatch" style="background:var(--wall)"></i>Obstaculo</span>
            <span><i class="swatch" style="background:var(--discovered)"></i>Descubierto/en estructura</span>
            <span><i class="swatch" style="background:var(--processed-bfs)"></i>Procesado BFS</span>
            <span><i class="swatch" style="background:var(--processed-dfs)"></i>Procesado DFS</span>
            <span><i class="swatch" style="background:var(--current)"></i>Nodo actual</span>
            <span><i class="swatch" style="background:var(--path)"></i>Ruta final</span>
        </section>
        <section class="compare">
            <article class="panel">
                <h2>BFS</h2>
                <p id="descBfs" class="desc"></p>
                <div class="grid-wrap"><div id="gridBfs" class="grid"></div></div>
                <div id="estructuraBfs" class="structure"></div>
            </article>
            <article class="panel">
                <h2>DFS</h2>
                <p id="descDfs" class="desc"></p>
                <div class="grid-wrap"><div id="gridDfs" class="grid"></div></div>
                <div id="estructuraDfs" class="structure"></div>
            </article>
        </section>
        <footer>
            Archivo generado desde {html.escape(str(MAPA_TXT.name))}. Para cambiar el mapa, ejecuta de nuevo la opcion 1 del programa Java y vuelve a generar esta animacion.
        </footer>
    </main>
    <script>
        const data = {json.dumps(datos, ensure_ascii=False)};
        const maxSteps = Math.max(data.bfs.length, data.dfs.length) - 1;
        const stepInput = document.getElementById("step");
        const stepLabel = document.getElementById("stepLabel");
        const playBtn = document.getElementById("play");
        let currentStep = 0;
        let timer = null;
        stepInput.max = maxSteps;

        function key(pos) {{
            return pos[0] + "-" + pos[1];
        }}

        function setFromList(items) {{
            return new Set((items || []).map(key));
        }}

        function frameAt(frames, step) {{
            return frames[Math.min(step, frames.length - 1)];
        }}

        function renderGrid(targetId, frames, kind, step) {{
            const target = document.getElementById(targetId);
            const frame = frameAt(frames, step);
            const cols = data.mapa[0].length;
            target.style.setProperty("--cols", cols);
            target.innerHTML = "";

            const descubiertos = setFromList(frame.descubiertos);
            const procesados = setFromList(frame.procesados);
            const ruta = setFromList(frame.ruta);
            const actual = frame.actual ? key(frame.actual) : "";
            const inicio = key(data.inicio);
            const destino = key(data.destino);

            for (let f = 0; f < data.mapa.length; f++) {{
                for (let c = 0; c < data.mapa[f].length; c++) {{
                    const id = f + "-" + c;
                    const cell = document.createElement("div");
                    cell.className = "cell";
                    cell.textContent = f + "," + c;

                    if (data.mapa[f][c] === 1) cell.classList.add("wall");
                    if (descubiertos.has(id)) cell.classList.add("discovered");
                    if (procesados.has(id)) cell.classList.add("processed", kind);
                    if (ruta.has(id)) cell.classList.add("path");
                    if (id === actual) cell.classList.add("current");
                    if (id === inicio) {{
                        cell.classList.add("start");
                        cell.textContent = "S";
                    }}
                    if (id === destino) {{
                        cell.classList.add("goal");
                        cell.textContent = "G";
                    }}
                    if (id === actual && id !== inicio && id !== destino) {{
                        cell.textContent = "A";
                    }}
                    target.appendChild(cell);
                }}
            }}
        }}

        function formatStructure(name, frame) {{
            const items = frame.estructura || [];
            if (!items.length) return name + ": vacia";
            const texto = items.map(pos => "(" + pos[0] + "," + pos[1] + ")").join(" -> ");
            return name + ": " + texto;
        }}

        function render() {{
            const bfs = frameAt(data.bfs, currentStep);
            const dfs = frameAt(data.dfs, currentStep);
            renderGrid("gridBfs", data.bfs, "bfs", currentStep);
            renderGrid("gridDfs", data.dfs, "dfs", currentStep);
            document.getElementById("descBfs").textContent = bfs.titulo + ". " + bfs.descripcion;
            document.getElementById("descDfs").textContent = dfs.titulo + ". " + dfs.descripcion;
            document.getElementById("estructuraBfs").textContent = formatStructure("Cola", bfs);
            document.getElementById("estructuraDfs").textContent = formatStructure("Pila", dfs);
            stepInput.value = currentStep;
            stepLabel.textContent = "Paso " + currentStep + " / " + maxSteps;
        }}

        function stop() {{
            if (timer) {{
                clearInterval(timer);
                timer = null;
            }}
            playBtn.textContent = "Reproducir";
        }}

        document.getElementById("prev").addEventListener("click", () => {{
            stop();
            currentStep = Math.max(0, currentStep - 1);
            render();
        }});

        document.getElementById("next").addEventListener("click", () => {{
            stop();
            currentStep = Math.min(maxSteps, currentStep + 1);
            render();
        }});

        playBtn.addEventListener("click", () => {{
            if (timer) {{
                stop();
                return;
            }}
            playBtn.textContent = "Pausar";
            timer = setInterval(() => {{
                if (currentStep >= maxSteps) {{
                    stop();
                    return;
                }}
                currentStep++;
                render();
            }}, 550);
        }});

        stepInput.addEventListener("input", () => {{
            stop();
            currentStep = Number(stepInput.value);
            render();
        }});

        render();
    </script>
</body>
</html>
"""
    ANIMACION_HTML.write_text(contenido, encoding="utf-8")


def main():
    mapa, inicio, destino = leer_mapa()
    frames_bfs, ruta_bfs = simular_bfs(mapa, inicio, destino)
    frames_dfs, ruta_dfs = simular_dfs(mapa, inicio, destino)
    generar_html(mapa, inicio, destino, frames_bfs, frames_dfs, ruta_bfs, ruta_dfs)
    print("Animacion generada correctamente.")
    print(f"- {ANIMACION_HTML}")
    print(f"Pasos BFS: {len(frames_bfs) - 1}")
    print(f"Pasos DFS: {len(frames_dfs) - 1}")


if __name__ == "__main__":
    main()
