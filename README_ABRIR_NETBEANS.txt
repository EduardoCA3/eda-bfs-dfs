PROYECTO NETBEANS - COMPARACION BFS Y DFS (JAVA 17)

Este proyecto esta armado como proyecto Java Ant de NetBeans:
- build.xml
- nbproject
- src/comparacionbfsdfs
- main.class=comparacionbfsdfs.Main
- javac.source=17
- javac.target=17

COMO ABRIRLO:
1. Descomprime el ZIP.
2. En NetBeans selecciona File > Open Project.
3. Selecciona la carpeta principal: ComparacionBFSDFS_NetBeans_Java17.
4. No abras la carpeta src.
5. Ejecuta la clase Main.java.

SI NETBEANS TE PIDE PLATAFORMA JAVA:
- Clic derecho al proyecto > Properties > Libraries.
- En Java Platform selecciona JDK 17.
- Luego Clean and Build.

SALIDAS:
Al ejecutar el proyecto se creara una carpeta salida_resultados con:
- detalle_resultados.csv
- resumen_resultados.csv
- equipo_ejecucion.txt
- mapa_ejemplo.txt
- proceso_prueba_simple.txt
- prueba_simple_resultados.csv
- animacion_grafos.html
- dashboard_prueba_simple.html
- proceso_comparacion.txt
- mapas_animacion_opcion2.txt
- dashboard_resultados.html
- animacion_opcion2.html

IMPORTANTE:
- La opcion 1 genera el mapa, el proceso, el CSV de la prueba simple,
  la animacion BFS/DFS y el grafico de barras de esa prueba.
- La opcion 2 genera los CSV completos de comparacion y el dashboard de
  graficos de barras, ademas de la animacion interactiva por escenarios.
- Si Python esta disponible en la PC, los graficos HTML se generan automaticamente.
- Para abrir la carpeta de salidas, usa ABRIR_SALIDA_RESULTADOS.bat.
- Para abrir los graficos HTML, usa ABRIR_GRAFICOS.bat.

ORDEN DE CLASES:
- Main: muestra el menu principal.
- ControladorExperimento: coordina la prueba simple y la comparacion completa.
- BFS y DFS: algoritmos principales. Pueden ejecutar en modo normal o en modo con proceso detallado.
- GrafoCuadricula: contiene reglas comunes de la cuadricula: celda libre, obstaculo, coordenadas y orden de movimiento.
- GeneradorEscenarios: crea mapas con obstaculos.
- ValidadorRuta: verifica que el mapa generado tenga camino disponible.
- ExportadorResultados: genera TXT y CSV.

USO EN VISUAL STUDIO CODE:
Tambien se agrego soporte para VS Code:
- .vscode/tasks.json: tareas para compilar, ejecutar y generar graficos.
- .vscode/launch.json: configuracion para depurar Main.java.
- scripts/generar_graficos.py: crea un dashboard HTML y graficos SVG desde resumen_resultados.csv.
- scripts/generar_grafico_prueba_simple.py: crea graficos de barras desde prueba_simple_resultados.csv.
- scripts/generar_animacion_grafos.py: crea una animacion HTML para ver el recorrido BFS y DFS paso a paso.
- README_VSCODE_GRAFICOS.txt: guia paso a paso para usarlo en VS Code.
