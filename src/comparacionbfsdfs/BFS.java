package comparacionbfsdfs;

public class BFS {

    public Resultado buscar(int[][] mapa, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino) {
        return buscarInterno(mapa, filaInicio, columnaInicio, filaDestino, columnaDestino, false);
    }

    public Resultado buscarConProceso(int[][] mapa, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino) {
        return buscarInterno(mapa, filaInicio, columnaInicio, filaDestino, columnaDestino, true);
    }

    private Resultado buscarInterno(int[][] mapa, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino, boolean mostrarProceso) {
        long inicioTiempo = System.nanoTime();

        int tamano = mapa.length;
        boolean[][] visitado = new boolean[tamano][tamano];
        int[][] padre = new int[tamano][tamano];
        inicializarPadres(padre);

        Cola cola = new Cola();
        StringBuilder proceso = new StringBuilder();

        int inicio = GrafoCuadricula.convertirAId(filaInicio, columnaInicio, tamano);
        int destino = GrafoCuadricula.convertirAId(filaDestino, columnaDestino, tamano);

        if (mostrarProceso) {
            agregarLinea(proceso, "BFS - Busqueda en anchura");
            agregarLinea(proceso, "Estructura usada: cola (FIFO).");
            agregarLinea(proceso, "Orden de revision: arriba, derecha, abajo, izquierda.");
            agregarLinea(proceso,
                    "Inicio: " + GrafoCuadricula.posicion(filaInicio, columnaInicio)
                    + " | Destino: " + GrafoCuadricula.posicion(filaDestino, columnaDestino));
        }

        cola.insertar(inicio);
        visitado[filaInicio][columnaInicio] = true;
        if (mostrarProceso) {
            agregarLinea(proceso,
                    "Se encola el nodo inicial "
                    + GrafoCuadricula.posicion(filaInicio, columnaInicio) + ".");
        }

        int nodosVisitados = 0;
        int paso = 1;
        boolean encontrado = false;

        while (!cola.esvacia()) {
            int actual = cola.desencolar();
            int filaActual = GrafoCuadricula.obtenerFila(actual, tamano);
            int columnaActual = GrafoCuadricula.obtenerColumna(actual, tamano);
            nodosVisitados++;

            if (mostrarProceso) {
                agregarLinea(proceso,
                        "Paso " + paso + ": se desencola "
                        + GrafoCuadricula.posicion(filaActual, columnaActual)
                        + ". Nodos visitados: " + nodosVisitados
                        + ". Elementos pendientes en cola: " + cola.cantidad() + ".");
            }

            if (actual == destino) {
                encontrado = true;
                if (mostrarProceso) {
                    agregarLinea(proceso, "Destino encontrado. Se detiene BFS.");
                }
                break;
            }

            for (int direccion = 0; direccion < GrafoCuadricula.DIRECCIONES.length; direccion++) {
                int nuevaFila = filaActual + GrafoCuadricula.CAMBIO_FILA[direccion];
                int nuevaColumna = columnaActual + GrafoCuadricula.CAMBIO_COLUMNA[direccion];
                String movimiento = GrafoCuadricula.DIRECCIONES[direccion];

                if (GrafoCuadricula.esCeldaLibre(mapa, nuevaFila, nuevaColumna)
                        && !visitado[nuevaFila][nuevaColumna]) {
                    visitado[nuevaFila][nuevaColumna] = true;
                    padre[nuevaFila][nuevaColumna] = actual;
                    cola.insertar(GrafoCuadricula.convertirAId(nuevaFila, nuevaColumna, tamano));
                    if (mostrarProceso) {
                        agregarLinea(proceso,
                                "  Revisa " + movimiento + " -> "
                                + GrafoCuadricula.posicion(nuevaFila, nuevaColumna)
                                + ": libre, se marca como visitado y se encola.");
                    }
                } else {
                    if (mostrarProceso) {
                        agregarLinea(proceso,
                                "  Revisa " + movimiento + " -> "
                                + GrafoCuadricula.posicion(nuevaFila, nuevaColumna)
                                + ": no se encola porque " + explicarNoEncolado(mapa,
                                        nuevaFila, nuevaColumna, visitado) + ".");
                    }
                }
            }
            paso++;
        }

        long finTiempo = System.nanoTime();
        double tiempoMs = (finTiempo - inicioTiempo) / 1000000.0;
        int longitud = encontrado ? calcularLongitud(padre, filaInicio, columnaInicio,
                filaDestino, columnaDestino) : -1;
        int memoria = cola.maxCantidad() + nodosVisitados;
        String rutaTexto = encontrado ? construirRutaTexto(padre, filaInicio, columnaInicio,
                filaDestino, columnaDestino) : "No se encontro ruta.";

        if (mostrarProceso) {
            agregarLinea(proceso, "Resumen BFS:");
            agregarLinea(proceso, "  Encontro ruta: " + (encontrado ? "si" : "no"));
            agregarLinea(proceso, "  Longitud de ruta: " + longitud);
            agregarLinea(proceso, "  Maximo de la cola: " + cola.maxCantidad());
            agregarLinea(proceso, "  Ruta: " + rutaTexto);
        }

        return new Resultado("BFS", encontrado, tiempoMs, nodosVisitados,
                longitud, cola.maxCantidad(), memoria, padre, rutaTexto, proceso.toString());
    }

    private String explicarNoEncolado(int[][] mapa, int fila, int columna, boolean[][] visitado) {
        if (!GrafoCuadricula.estaDentro(mapa, fila, columna)) {
            return "esta fuera del mapa";
        }
        if (mapa[fila][columna] == GrafoCuadricula.OBSTACULO) {
            return "es un obstaculo";
        }
        if (visitado[fila][columna]) {
            return "ya fue visitado";
        }
        return "no cumple una condicion de BFS";
    }

    private void inicializarPadres(int[][] padre) {
        for (int fila = 0; fila < padre.length; fila++) {
            for (int columna = 0; columna < padre.length; columna++) {
                padre[fila][columna] = -1;
            }
        }
    }

    private int calcularLongitud(int[][] padre, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino) {
        int tamano = padre.length;
        int actual = GrafoCuadricula.convertirAId(filaDestino, columnaDestino, tamano);
        int inicio = GrafoCuadricula.convertirAId(filaInicio, columnaInicio, tamano);
        int pasos = 0;

        while (actual != inicio && actual != -1) {
            int fila = GrafoCuadricula.obtenerFila(actual, tamano);
            int columna = GrafoCuadricula.obtenerColumna(actual, tamano);
            actual = padre[fila][columna];
            pasos++;
        }
        return pasos;
    }

    private String construirRutaTexto(int[][] padre, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino) {
        int tamano = padre.length;
        int[] ruta = new int[tamano * tamano];
        int cantidad = 0;
        int actual = GrafoCuadricula.convertirAId(filaDestino, columnaDestino, tamano);
        int inicio = GrafoCuadricula.convertirAId(filaInicio, columnaInicio, tamano);

        while (actual != -1 && cantidad < ruta.length) {
            ruta[cantidad] = actual;
            cantidad++;
            if (actual == inicio) {
                break;
            }
            int fila = GrafoCuadricula.obtenerFila(actual, tamano);
            int columna = GrafoCuadricula.obtenerColumna(actual, tamano);
            actual = padre[fila][columna];
        }

        if (cantidad == 0 || ruta[cantidad - 1] != inicio) {
            return "No se pudo reconstruir la ruta.";
        }

        StringBuilder rutaTexto = new StringBuilder();
        for (int i = cantidad - 1; i >= 0; i--) {
            int fila = GrafoCuadricula.obtenerFila(ruta[i], tamano);
            int columna = GrafoCuadricula.obtenerColumna(ruta[i], tamano);
            rutaTexto.append(GrafoCuadricula.posicion(fila, columna));
            if (i > 0) {
                rutaTexto.append(" -> ");
            }
        }
        return rutaTexto.toString();
    }

    private void agregarLinea(StringBuilder proceso, String texto) {
        proceso.append(texto).append(System.lineSeparator());
    }
}
