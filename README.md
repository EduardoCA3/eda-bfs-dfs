# Comparación de BFS y DFS en un campus

Proyecto académico de Estructuras de Datos y Algoritmos que compara BFS y DFS al buscar rutas sobre mapas de cuadrícula que representan un campus.

## Contenido

- Implementaciones propias de cola, pila, BFS y DFS en Java 17.
- Generación de escenarios con obstáculos.
- Medición de tiempo, nodos visitados, longitud de ruta y memoria aproximada.
- Exportación de resultados a CSV y texto.
- Scripts de Python para crear gráficos, dashboards y animaciones.

## Ejecución

Abre el proyecto en NetBeans con Java 17 y ejecuta `comparacionbfsdfs.Main`. También puede compilarse con Ant:

```bash
ant clean jar
java -jar dist/ComparacionBFSDFS.jar
```

Los resultados generados se guardan en `salida_resultados/`. El archivo que registra información local del equipo está excluido de Git.
