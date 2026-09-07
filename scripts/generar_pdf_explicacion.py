from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output" / "pdf"
PDF_PATH = OUTPUT_DIR / "explicacion_proyecto_bfs_dfs.pdf"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCustom",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=31,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "Heading1Custom",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=23,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2Custom",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "BodyCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=13.6,
            textColor=colors.HexColor("#111827"),
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "SmallCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            textColor=colors.HexColor("#4b5563"),
        ),
        "bullet": ParagraphStyle(
            "BulletCustom",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.5,
            leftIndent=10,
            textColor=colors.HexColor("#111827"),
        ),
        "code": ParagraphStyle(
            "CodeCustom",
            fontName="Courier",
            fontSize=7.6,
            leading=9.4,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f3f4f6"),
            borderColor=colors.HexColor("#d1d5db"),
            borderWidth=0.5,
            borderPadding=6,
            spaceAfter=8,
        ),
        "box": ParagraphStyle(
            "BoxCustom",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
        ),
    }


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(item, style), leftIndent=8) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontSize=7,
    )


def section(title, story, st):
    story.append(p(title, st["h1"]))


def subsection(title, story, st):
    story.append(p(title, st["h2"]))


def make_table(data, widths, header=True):
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d1d5db")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    table.setStyle(TableStyle(style))
    return table


def flow_diagram(st):
    cells = [
        ["Main.java\nmenu"],
        ["->"],
        ["ControladorExperimento\ncoordina opcion 1 u opcion 2"],
        ["->"],
        ["GeneradorEscenarios\ncrea mapas validos"],
        ["->"],
        ["BFS.java y DFS.java\nejecutan busqueda"],
        ["->"],
        ["Resultado.java\nguarda metricas"],
        ["->"],
        ["ExportadorResultados\ngenera TXT y CSV"],
        ["->"],
        ["Python + HTML\ncrea graficos y animaciones"],
    ]
    data = [[p(text.replace("\n", "<br/>"), st["box"])] for row in cells for text in row]
    table = Table(data, colWidths=[14.8 * cm])
    table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#e0f2fe")),
                ("BACKGROUND", (0, 2), (0, 2), colors.HexColor("#dbeafe")),
                ("BACKGROUND", (0, 4), (0, 4), colors.HexColor("#fef3c7")),
                ("BACKGROUND", (0, 6), (0, 6), colors.HexColor("#dcfce7")),
                ("BACKGROUND", (0, 8), (0, 8), colors.HexColor("#ede9fe")),
                ("BACKGROUND", (0, 10), (0, 10), colors.HexColor("#ffedd5")),
                ("BACKGROUND", (0, 12), (0, 12), colors.HexColor("#f3f4f6")),
                ("TEXTCOLOR", (0, 1), (0, 11), colors.HexColor("#6b7280")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def draw_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5 * cm, 1.0 * cm, "Explicacion del proyecto BFS vs DFS")
    canvas.drawRightString(width - 1.5 * cm, 1.0 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    st = styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.45 * cm,
        title="Explicacion proyecto BFS DFS",
        author="Proyecto Comparacion BFS DFS",
    )

    story = []
    story.append(Spacer(1, 1.2 * cm))
    story.append(p("Explicacion del proyecto BFS vs DFS", st["title"]))
    story.append(
        p(
            "Guia general y detallada del codigo, pensada para explicar el proyecto "
            "aunque la persona no conozca mucho de programacion.",
            st["subtitle"],
        )
    )
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        make_table(
            [
                [p("<b>Proyecto</b>", st["body"]), p("Comparacion de algoritmos BFS y DFS sobre mapas tipo cuadricula.", st["body"])],
                [p("<b>Lenguaje principal</b>", st["body"]), p("Java 17, ejecutado desde NetBeans.", st["body"])],
                [p("<b>Lenguaje de apoyo</b>", st["body"]), p("Python, usado para convertir resultados en graficos y animaciones HTML.", st["body"])],
                [p("<b>Resultado principal</b>", st["body"]), p("TXT, CSV, dashboards HTML, SVG y animaciones interactivas.", st["body"])],
            ],
            [4.2 * cm, 10.6 * cm],
            header=False,
        )
    )
    story.append(Spacer(1, 0.5 * cm))
    story.append(p("Idea corta para exponer", st["h2"]))
    story.append(
        p(
            "El proyecto compara dos formas de recorrer un grafo: BFS y DFS. "
            "El grafo se representa como una matriz, donde cada celda puede estar libre "
            "o bloqueada por un obstaculo. El programa mide tiempo, cantidad de nodos "
            "visitados, longitud de ruta y memoria aproximada. Luego exporta esos datos "
            "para verlos en archivos y graficos.",
            st["body"],
        )
    )
    story.append(PageBreak())

    section("1. Explicacion general para principiantes", story, st)
    story.append(
        p(
            "El programa no trabaja con calles reales ni con imagenes. Trabaja con una "
            "cuadricula: una tabla de filas y columnas. El inicio esta en la esquina "
            "superior izquierda y el destino en la esquina inferior derecha. Algunas "
            "celdas son obstaculos y no se pueden pisar.",
            st["body"],
        )
    )
    story.append(
        p(
            "BFS y DFS reciben exactamente el mismo mapa. Esa parte es importante, porque "
            "asi la comparacion es justa: si uno visita mas nodos o encuentra una ruta "
            "distinta, es por su estrategia de busqueda, no porque el mapa haya cambiado.",
            st["body"],
        )
    )

    subsection("Lenguajes usados", story, st)
    story.append(
        make_table(
            [
                [p("<b>Lenguaje</b>", st["body"]), p("<b>Para que se usa</b>", st["body"]), p("<b>Por que sirve aqui</b>", st["body"])],
                [p("Java 17", st["body"]), p("Menu, algoritmos, mapas, mediciones y exportacion.", st["body"]), p("Es el lenguaje principal del curso y se ejecuta bien en NetBeans.", st["body"])],
                [p("Python", st["body"]), p("Lee CSV/TXT y genera HTML/SVG.", st["body"]), p("Permite crear graficos sin cambiar el algoritmo en Java.", st["body"])],
                [p("HTML/CSS/JavaScript", st["body"]), p("Muestra dashboards y animaciones en el navegador.", st["body"]), p("Sirve para avanzar, retroceder y reproducir el recorrido visualmente.", st["body"])],
                [p("CSV y TXT", st["body"]), p("Guardan datos numericos y procesos.", st["body"]), p("Son archivos faciles de revisar y reutilizar.", st["body"])],
            ],
            [3.0 * cm, 5.8 * cm, 6.0 * cm],
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(p("Flujo general del sistema", st["h2"]))
    story.append(flow_diagram(st))
    story.append(PageBreak())

    section("2. Opciones del programa", story, st)
    story.append(
        p(
            "El menu actual tiene dos opciones utiles para la entrega: una prueba simple "
            "para ver el proceso paso a paso y una comparacion completa para obtener "
            "datos estadisticos y graficos.",
            st["body"],
        )
    )
    story.append(
        make_table(
            [
                [p("<b>Opcion</b>", st["body"]), p("<b>Que hace</b>", st["body"]), p("<b>Que archivos genera</b>", st["body"])],
                [
                    p("1. Prueba simple 10x10", st["body"]),
                    p("Genera un mapa pequeno y ejecuta BFS y DFS con proceso detallado.", st["body"]),
                    p("mapa_ejemplo.txt, proceso_prueba_simple.txt, prueba_simple_resultados.csv, animacion_grafos.html, dashboard_prueba_simple.html", st["body"]),
                ],
                [
                    p("2. Comparacion completa", st["body"]),
                    p("Prueba mapas 10x10, 20x20 y 50x50 con 10%, 20% y 30% de obstaculos. Cada escenario se repite 30 veces.", st["body"]),
                    p("detalle_resultados.csv, resumen_resultados.csv, proceso_comparacion.txt, mapas_animacion_opcion2.txt, dashboard_resultados.html, animacion_opcion2.html", st["body"]),
                ],
            ],
            [3.5 * cm, 5.6 * cm, 5.7 * cm],
        )
    )
    subsection("Por que se quito la opcion 3", story, st)
    story.append(
        p(
            "La opcion del campus fue retirada para que el proyecto quede enfocado en la "
            "comparacion real entre BFS y DFS. Esa opcion podia hacer la entrega mas larga "
            "sin aportar mucho a las metricas principales. Ahora el programa es mas claro "
            "y menos pesado.",
            st["body"],
        )
    )

    section("3. Explicacion detallada del codigo Java", story, st)
    subsection("Main.java", story, st)
    story.append(
        p(
            "Es la entrada del programa. Muestra el menu, lee la opcion del usuario con "
            "Scanner y llama al metodo correcto del controlador.",
            st["body"],
        )
    )
    story.append(
        Preformatted(
            "ControladorExperimento controlador = new ControladorExperimento();\n"
            "op = entrada.nextInt();\n\n"
            "switch (op) {\n"
            "    case 1: controlador.ejecutarPruebaSimple(); break;\n"
            "    case 2: controlador.ejecutarComparacionCompleta(); break;\n"
            "    case 0: System.out.println(\"Programa finalizado.\"); break;\n"
            "}",
            st["code"],
        )
    )

    subsection("ControladorExperimento.java", story, st)
    story.append(
        p(
            "Es la clase que organiza todo. No contiene el algoritmo en si, sino que "
            "coordina el experimento: crea mapas, llama a BFS y DFS, guarda archivos y "
            "ejecuta Python para generar graficos.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>tamanos</b>: usa 10, 20 y 50 para probar mapas de diferentes dimensiones.",
                "<b>porcentajesObstaculos</b>: usa 10%, 20% y 30% para cambiar dificultad.",
                "<b>repeticiones</b>: ejecuta 30 repeticiones por escenario para promediar.",
                "<b>ejecutarPruebaSimple</b>: hace una demostracion pequena y detallada.",
                "<b>ejecutarComparacionCompleta</b>: crea la base de datos completa para comparar.",
            ],
            st["bullet"],
        )
    )
    story.append(
        p(
            "En la opcion 2 se recorre cada tamano y cada porcentaje de obstaculos. En "
            "cada combinacion se ejecutan 30 mapas. Luego se calculan promedio, mediana "
            "y desviacion para comparar con mas seriedad.",
            st["body"],
        )
    )

    subsection("GrafoCuadricula.java", story, st)
    story.append(
        p(
            "Define las reglas comunes de la cuadricula. Aqui se dice que 0 es celda libre "
            "y 1 es obstaculo. Tambien se define el orden de movimiento: arriba, derecha, "
            "abajo e izquierda.",
            st["body"],
        )
    )
    story.append(
        Preformatted(
            "public static final int LIBRE = 0;\n"
            "public static final int OBSTACULO = 1;\n"
            "public static final int[] CAMBIO_FILA = {-1, 0, 1, 0};\n"
            "public static final int[] CAMBIO_COLUMNA = {0, 1, 0, -1};",
            st["code"],
        )
    )
    story.append(
        p(
            "Tambien convierte una posicion de dos dimensiones a un identificador entero. "
            "Por ejemplo, en un mapa de tamano 10, la celda fila 2 columna 3 se convierte "
            "en 2 * 10 + 3 = 23.",
            st["body"],
        )
    )

    subsection("BFS.java", story, st)
    story.append(
        p(
            "BFS significa busqueda en anchura. Explora por niveles: primero revisa los "
            "vecinos cercanos al inicio, luego los vecinos de esos vecinos, y asi avanza. "
            "Para lograrlo usa una cola, que funciona como FIFO: el primero que entra es "
            "el primero que sale.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "Crea una matriz <b>visitado</b> para no repetir celdas.",
                "Crea una matriz <b>padre</b> para reconstruir la ruta final.",
                "Inserta el inicio en la cola.",
                "Mientras la cola no este vacia, saca un nodo, revisa vecinos y encola los validos.",
                "Cuando llega al destino, reconstruye la ruta desde el destino hacia el inicio.",
            ],
            st["bullet"],
        )
    )
    story.append(
        Preformatted(
            "cola.insertar(inicio);\n"
            "visitado[filaInicio][columnaInicio] = true;\n\n"
            "while (!cola.esvacia()) {\n"
            "    int actual = cola.desencolar();\n"
            "    // revisa vecinos libres y no visitados\n"
            "}",
            st["code"],
        )
    )
    story.append(
        p(
            "BFS suele encontrar la ruta con menor cantidad de tramos cuando el grafo no "
            "tiene pesos. Por eso es importante para comparar la longitud de ruta.",
            st["body"],
        )
    )

    subsection("DFS.java", story, st)
    story.append(
        p(
            "DFS significa busqueda en profundidad. En vez de explorar por niveles, intenta "
            "avanzar lo mas profundo posible por un camino. Para lograrlo usa una pila, que "
            "funciona como LIFO: el ultimo que entra es el primero que sale.",
            st["body"],
        )
    )
    story.append(
        bullets(
            [
                "Usa <b>descubierto</b> para evitar meter la misma celda varias veces en la pila.",
                "Usa <b>visitado</b> para confirmar que una celda ya fue procesada.",
                "Apila el inicio y luego desapila el ultimo nodo agregado.",
                "Apila vecinos libres en orden inverso para respetar el orden visual de exploracion.",
                "Puede llegar rapido, pero no garantiza la ruta mas corta.",
            ],
            st["bullet"],
        )
    )
    story.append(
        Preformatted(
            "pila.push(inicio);\n"
            "descubierto[filaInicio][columnaInicio] = true;\n\n"
            "while (!pila.esvacia()) {\n"
            "    int actual = pila.pop();\n"
            "    // revisa vecinos y apila los validos\n"
            "}",
            st["code"],
        )
    )

    subsection("Cola.java, Pila.java y Nodo.java", story, st)
    story.append(
        p(
            "Estas clases implementan las estructuras de datos manualmente con nodos enlazados. "
            "No se usa directamente una cola o pila de Java, sino una version propia para que "
            "el funcionamiento sea visible y entendible.",
            st["body"],
        )
    )
    story.append(
        make_table(
            [
                [p("<b>Clase</b>", st["body"]), p("<b>Funcion</b>", st["body"])],
                [p("Nodo", st["body"]), p("Guarda un valor entero y una referencia al siguiente nodo.", st["body"])],
                [p("Cola", st["body"]), p("Tiene front y rear. Inserta al final y desencola por el inicio.", st["body"])],
                [p("Pila", st["body"]), p("Tiene top. Inserta y retira siempre por la parte superior.", st["body"])],
            ],
            [3.2 * cm, 11.6 * cm],
        )
    )
    story.append(PageBreak())

    subsection("Resultado.java", story, st)
    story.append(
        p(
            "Es una clase contenedora. Guarda lo que devuelve BFS o DFS: nombre del algoritmo, "
            "si encontro ruta, tiempo en milisegundos, nodos visitados, longitud de ruta, "
            "maximo de cola o pila, memoria aproximada, matriz de padres, ruta en texto y "
            "proceso detallado.",
            st["body"],
        )
    )

    subsection("GeneradorEscenarios.java", story, st)
    story.append(
        p(
            "Crea mapas aleatorios con obstaculos. Usa una semilla para que el mapa se pueda "
            "reproducir. Nunca coloca obstaculos en el inicio ni en el destino.",
            st["body"],
        )
    )
    story.append(
        p(
            "Despues llama a ValidadorRuta para confirmar que existe al menos una ruta. Si no "
            "existe, genera otro mapa con una semilla distinta hasta conseguir uno valido.",
            st["body"],
        )
    )

    subsection("ValidadorRuta.java", story, st)
    story.append(
        p(
            "Usa BFS como verificador. Si BFS logra llegar al destino, entonces el mapa sirve "
            "para la prueba. Si no llega, el mapa se descarta porque no permitiria comparar "
            "bien a BFS y DFS.",
            st["body"],
        )
    )

    subsection("ExportadorResultados.java", story, st)
    story.append(
        p(
            "Crea la carpeta salida_resultados y guarda los archivos. En la opcion 1 guarda "
            "el mapa, el proceso paso a paso y un CSV pequeno. En la opcion 2 se usan "
            "escritores para guardar detalle_resultados.csv, resumen_resultados.csv, "
            "proceso_comparacion.txt y mapas_animacion_opcion2.txt.",
            st["body"],
        )
    )

    subsection("EjecutorPython.java", story, st)
    story.append(
        p(
            "Esta clase conecta Java con Python. Intenta ejecutar los scripts con el comando "
            "python. Si no funciona, prueba con py. Si tampoco puede, muestra el comando para "
            "ejecutarlo manualmente.",
            st["body"],
        )
    )

    section("4. Como se calculan las metricas", story, st)
    story.append(
        make_table(
            [
                [p("<b>Metrica</b>", st["body"]), p("<b>Como se obtiene</b>", st["body"]), p("<b>Que significa</b>", st["body"])],
                [p("tiempoMs", st["body"]), p("Se mide con System.nanoTime antes y despues del algoritmo.", st["body"]), p("Cuanto tarda la busqueda.", st["body"])],
                [p("nodosVisitados", st["body"]), p("Se incrementa cada vez que se procesa una celda.", st["body"]), p("Cuanto exploro el algoritmo.", st["body"])],
                [p("longitudRuta", st["body"]), p("Se reconstruye con la matriz padre desde destino hasta inicio.", st["body"]), p("Cantidad de tramos de la ruta final.", st["body"])],
                [p("maxColaPila", st["body"]), p("La cola o pila guarda su mayor cantidad de elementos.", st["body"]), p("Pico de uso de estructura.", st["body"])],
                [p("memoriaAprox", st["body"]), p("nodosVisitados + maxColaPila.", st["body"]), p("Estimacion simple para comparar consumo.", st["body"])],
            ],
            [3.0 * cm, 6.0 * cm, 5.8 * cm],
        )
    )
    story.append(PageBreak())

    section("5. Scripts Python y visualizaciones", story, st)
    story.append(
        p(
            "Python no decide quien gana ni cambia el experimento. Su trabajo es leer los "
            "archivos que produjo Java y convertirlos en graficos o animaciones.",
            st["body"],
        )
    )
    story.append(
        make_table(
            [
                [p("<b>Script</b>", st["body"]), p("<b>Entrada</b>", st["body"]), p("<b>Salida</b>", st["body"])],
                [p("generar_animacion_grafos.py", st["body"]), p("mapa_ejemplo.txt", st["body"]), p("animacion_grafos.html para opcion 1", st["body"])],
                [p("generar_grafico_prueba_simple.py", st["body"]), p("prueba_simple_resultados.csv", st["body"]), p("dashboard_prueba_simple.html y SVG", st["body"])],
                [p("generar_graficos.py", st["body"]), p("resumen_resultados.csv", st["body"]), p("dashboard_resultados.html y SVG", st["body"])],
                [p("generar_animacion_opcion2.py", st["body"]), p("mapas_animacion_opcion2.txt", st["body"]), p("animacion_opcion2.html con selector de escenarios", st["body"])],
            ],
            [5.0 * cm, 4.2 * cm, 5.6 * cm],
        )
    )
    subsection("Como funcionan las animaciones", story, st)
    story.append(
        p(
            "Los HTML contienen JavaScript. Ese JavaScript simula el recorrido paso a paso "
            "y guarda cada estado como un frame: nodo actual, nodos descubiertos, nodos "
            "procesados, cola o pila y ruta final. Por eso puedes presionar Anterior, "
            "Siguiente o Reproducir.",
            st["body"],
        )
    )
    story.append(
        p(
            "En la opcion 2 no se guardan las 30 repeticiones completas como animacion, porque "
            "seria muy pesado. Se guarda un mapa representativo por escenario: la primera "
            "repeticion de cada combinacion de tamano y porcentaje de obstaculos.",
            st["body"],
        )
    )

    section("6. Extensiones y herramientas usadas", story, st)
    story.append(
        p(
            "Para NetBeans no se necesita una extension especial: se necesita JDK 17 y el "
            "proyecto Java Ant. Para Visual Studio Code, las extensiones son de apoyo, no "
            "son obligatorias para que el codigo exista.",
            st["body"],
        )
    )
    story.append(
        make_table(
            [
                [p("<b>Herramienta</b>", st["body"]), p("<b>Uso</b>", st["body"])],
                [p("NetBeans", st["body"]), p("Abrir, compilar y ejecutar el proyecto Java.", st["body"])],
                [p("JDK 17", st["body"]), p("Compilar y ejecutar Java.", st["body"])],
                [p("Python", st["body"]), p("Ejecutar scripts que generan graficos y animaciones.", st["body"])],
                [p("VS Code - Extension Pack for Java", st["body"]), p("Editar, compilar y ejecutar Java desde VS Code.", st["body"])],
                [p("VS Code - Python", st["body"]), p("Ejecutar y editar scripts Python.", st["body"])],
                [p("Data Wrangler y Rainbow CSV", st["body"]), p("Ver CSV de forma mas comoda.", st["body"])],
                [p("Jupyter", st["body"]), p("Opcional para analizar datos si se quisiera hacer una exploracion extra.", st["body"])],
            ],
            [5.4 * cm, 9.4 * cm],
        )
    )

    section("7. Como explicarlo oralmente", story, st)
    story.append(
        p(
            "Una forma simple de explicarlo seria la siguiente:",
            st["body"],
        )
    )
    story.append(
        Preformatted(
            "Mi proyecto compara BFS y DFS en mapas representados como cuadriculas.\n"
            "Java genera los mapas, ejecuta ambos algoritmos y guarda las metricas.\n"
            "BFS usa una cola, por eso explora por niveles.\n"
            "DFS usa una pila, por eso profundiza por un camino antes de probar otros.\n"
            "Luego Python lee los CSV y TXT que genera Java y crea graficos HTML/SVG.\n"
            "La opcion 1 sirve para ver el proceso paso a paso.\n"
            "La opcion 2 sirve para comparar varios escenarios y ver resultados promedio.",
            st["code"],
        )
    )

    section("8. Archivos principales del proyecto", story, st)
    file_rows = [
        [p("<b>Archivo</b>", st["body"]), p("<b>Rol dentro del proyecto</b>", st["body"])],
        [p("Main.java", st["body"]), p("Menu principal.", st["body"])],
        [p("ControladorExperimento.java", st["body"]), p("Coordina pruebas, comparacion, archivos y Python.", st["body"])],
        [p("BFS.java", st["body"]), p("Busqueda en anchura con cola.", st["body"])],
        [p("DFS.java", st["body"]), p("Busqueda en profundidad con pila.", st["body"])],
        [p("GrafoCuadricula.java", st["body"]), p("Reglas de la matriz y movimientos.", st["body"])],
        [p("Cola.java / Pila.java / Nodo.java", st["body"]), p("Estructuras de datos propias.", st["body"])],
        [p("Resultado.java", st["body"]), p("Guarda metricas y proceso.", st["body"])],
        [p("GeneradorEscenarios.java", st["body"]), p("Crea mapas aleatorios validos.", st["body"])],
        [p("ValidadorRuta.java", st["body"]), p("Verifica que exista camino.", st["body"])],
        [p("ExportadorResultados.java", st["body"]), p("Crea TXT y CSV.", st["body"])],
        [p("EjecutorPython.java", st["body"]), p("Lanza scripts Python desde Java.", st["body"])],
        [p("scripts/*.py", st["body"]), p("Generan dashboards y animaciones.", st["body"])],
        [p("ABRIR_GRAFICOS.bat", st["body"]), p("Abre los HTML generados.", st["body"])],
    ]
    story.append(make_table(file_rows, [5.0 * cm, 9.8 * cm]))

    section("9. Conclusion", story, st)
    story.append(
        p(
            "El proyecto queda dividido de forma entendible: Java realiza la logica y la "
            "medicion; Python transforma resultados en graficos; HTML y JavaScript permiten "
            "ver el proceso de manera interactiva. Asi se puede explicar tanto el algoritmo "
            "como la forma en que se generan las salidas visuales.",
            st["body"],
        )
    )

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return PDF_PATH


if __name__ == "__main__":
    ruta = build_pdf()
    print(ruta)
