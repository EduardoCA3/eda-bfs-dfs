GUIA PARA USAR EL PROYECTO EN VISUAL STUDIO CODE

1. EXTENSIONES RECOMENDADAS

Instala estas extensiones desde VS Code:

- Extension Pack for Java
- Python
- Jupyter
- Data Wrangler
- Rainbow CSV

La extension de Python ayuda a ejecutar el script de graficos.
Data Wrangler y Rainbow CSV ayudan a revisar los archivos CSV de salida.


2. COMO ABRIR EL PROYECTO

En VS Code:

1. File > Open Folder.
2. Selecciona esta carpeta:

C:\Users\Usuario\Downloads\ComparacionBFSDFS_Campus_NetBeans_Java17\ComparacionBFSDFS_Campus_NetBeans_Java17

No abras solamente la carpeta src.


3. COMO EJECUTAR DESDE VS CODE

Opcion grafica con tareas:

1. En VS Code presiona Ctrl + Shift + P.
2. Escribe: Tasks: Run Task
3. Elige una de estas tareas:

- Compilar Java
- Ejecutar menu
- Ejecutar prueba simple
- Generar CSV comparacion
- Generar graficos HTML
- Abrir dashboard grafico
- Generar animacion BFS DFS
- Abrir grafico prueba simple
- Abrir animacion BFS DFS
- Abrir animacion opcion 2

La tarea mas completa es:

Abrir dashboard grafico

Esa tarea compila el proyecto, ejecuta la comparacion completa, genera los CSV,
crea los graficos y abre el dashboard HTML en el navegador.

Para la opcion 1, puedes usar:

Ejecutar prueba simple

Esa tarea ahora genera automaticamente:

- prueba_simple_resultados.csv
- animacion_grafos.html
- dashboard_prueba_simple.html

Para ver como cambia el grafo paso a paso, usa esta tarea:

Abrir animacion BFS DFS

Esa tarea ejecuta la prueba simple, genera el mapa de ejemplo y abre una
visualizacion interactiva donde BFS y DFS avanzan lado a lado.


4. COMO EJECUTAR DESDE TERMINAL DE VS CODE

Abre la terminal con:

Ctrl + ñ

Compilar:

javac -encoding UTF-8 -d build\classes src\comparacionbfsdfs\*.java

Ejecutar menu:

java -cp build\classes comparacionbfsdfs.Main

Generar la comparacion completa:

echo 2 | java -cp build\classes comparacionbfsdfs.Main

Generar graficos:

python scripts\generar_graficos.py

Generar grafico de barras de la prueba simple:

python scripts\generar_grafico_prueba_simple.py

Generar animacion del recorrido BFS y DFS:

python scripts\generar_animacion_grafos.py

Generar animacion de la opcion 2:

python scripts\generar_animacion_opcion2.py


5. ARCHIVOS GRAFICOS GENERADOS

El script crea estos archivos:

- salida_resultados\dashboard_resultados.html
- salida_resultados\animacion_grafos.html
- salida_resultados\animacion_opcion2.html
- salida_resultados\dashboard_prueba_simple.html
- salida_resultados\prueba_simple_resultados.csv
- salida_resultados\mapas_animacion_opcion2.txt
- salida_resultados\graficos\tiempo_promedio.svg
- salida_resultados\graficos\nodos_visitados.svg
- salida_resultados\graficos\longitud_ruta.svg
- salida_resultados\graficos\memoria_aproximada.svg

El HTML es para ver todo junto.
Los SVG son graficos individuales que puedes insertar en Word, PowerPoint o el informe.

El archivo animacion_grafos.html muestra el cambio del grafo paso a paso:

- Obstaculos
- Nodos descubiertos
- Nodo actual
- Nodos procesados por BFS
- Nodos procesados por DFS
- Ruta final encontrada


6. SI NO ABRE EL DASHBOARD

Abre manualmente este archivo con doble clic:

salida_resultados\dashboard_resultados.html

Para abrir la animacion:

salida_resultados\animacion_grafos.html

Para abrir la animacion de la opcion 2:

salida_resultados\animacion_opcion2.html

Para abrir las barras de la prueba simple:

salida_resultados\dashboard_prueba_simple.html

Tambien puedes dar doble clic a:

ABRIR_GRAFICOS.bat

Si VS Code dice que python no existe, instala Python o revisa que este en el PATH.
En esta PC ya se detecto Python 3.11.9 desde la terminal.
