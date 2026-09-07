package comparacionbfsdfs;

public class DFS {

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
        boolean[][] descubierto = new boolean[tamano][tamano];
        int[][] padre = new int[tamano][tamano];
        inicializarPadres(padre);

        Pila pila = new Pila();
        StringBuilder proceso = new StringBuilder();

        int inicio = GrafoCuadricula.convertirAId(filaInicio, columnaInicio, tamano);
        int destino = GrafoCuadricula.convertirAId(filaDestino, columnaDestino, tamano);

        if (mostrarProceso) {
            agregarLinea(proceso, "DFS - Busqueda en profundidad");
            agregarLinea(proceso, "Estructura usada: pila (LIFO).");
            agregarLinea(proceso, "Orden de exploracion buscado: arriba, derecha, abajo, izquierda.");
            agregarLinea(proceso,
                    "Como la pila saca el ultimo que entra, los vecinos se apilan en orden inverso.");
            agregarLinea(proceso,
                    "Inicio: " + GrafoCuadricula.posicion(filaInicio, columnaInicio)
                    + " | Destino: " + GrafoCuadricula.posicion(filaDestino, columnaDestino));
        }

        pila.push(inicio);
        descubierto[filaInicio][columnaInicio] = true;
        if (mostrarProceso) {
            agregarLinea(proceso,
                    "Se apila el nodo inicial "
                    + GrafoCuadricula.posicion(filaInicio, columnaInicio) + ".");
        }

        int nodosVisitados = 0;
        int paso = 1;
        boolean encontrado = false;

        while (!pila.esvacia()) {
            int actual = pila.pop();
            int filaActual = GrafoCuadricula.obtenerFila(actual, tamano);
            int columnaActual = GrafoCuadricula.obtenerColumna(actual, tamano);

            if (mostrarProceso) {
                agregarLinea(proceso,
                        "Paso " + paso + ": se desapila "
                        + GrafoCuadricula.posicion(filaActual, columnaActual)
                        + ". Elementos pendientes en pila: " + pila.cantidad() + ".");
            }

            if (visitado[filaActual][columnaActual]) {
                if (mostrarProceso) {
                    agregarLinea(proceso, "  Este nodo ya estaba visitado, por eso se ignora.");
                }
                paso++;
                continue;
            }

            visitado[filaActual][columnaActual] = true;
            nodosVisitados++;
            if (mostrarProceso) {
                agregarLinea(proceso,
                        "  Se marca como visitado. Nodos visitados: " + nodosVisitados + ".");
            }

            if (actual == destino) {
                encontrado = true;
                if (mostrarProceso) {
                    agregarLinea(proceso, "Destino encontrado. Se detiene DFS.");
                }
                break;
            }

            for (int direccion = GrafoCuadricula.DIRECCIONES.length - 1; direccion >= 0; direccion--) {
                int nuevaFila = filaActual + GrafoCuadricula.CAMBIO_FILA[direccion];
                int nuevaColumna = columnaActual + GrafoCuadricula.CAMBIO_COLUMNA[direccion];
                String movimiento = GrafoCuadricula.DIRECCIONES[direccion];

                if (GrafoCuadricula.esCeldaLibre(mapa, nuevaFila, nuevaColumna)
                        && !descubierto[nuevaFila][nuevaColumna]) {
                    descubierto[nuevaFila][nuevaColumna] = true;
                    padre[nuevaFila][nuevaColumna] = actual;
                    pila.push(GrafoCuadricula.convertirAId(nuevaFila, nuevaColumna, tamano));
                    if (mostrarProceso) {
                        agregarLinea(proceso,
                                "  Revisa " + movimiento + " -> "
                                + GrafoCuadricula.posicion(nuevaFila, nuevaColumna)
                                + ": libre, se descubre y se apila.");
                    }
                } else {
                    if (mostrarProceso) {
                        agregarLinea(proceso,
                                "  Revisa " + movimiento + " -> "
                                + GrafoCuadricula.posicion(nuevaFila, nuevaColumna)
                                + ": no se apila porque " + explicarNoApilado(mapa,
                                        nuevaFila, nuevaColumna, descubierto) + ".");
                    }
                }
            }
            paso++;
        }

        long finTiempo = System.nanoTime();
        double tiempoMs = (finTiempo - inicioTiempo) / 1000000.0;
        int longitud = encontrado ? calcularLongitud(padre, filaInicio, columnaInicio,
                filaDestino, columnaDestino) : -1;
        int memoria = pila.maxCantidad() + nodosVisitados;
        String rutaTexto = encontrado ? construirRutaTexto(padre, filaInicio, columnaInicio,
                filaDestino, columnaDestino) : "No se encontro ruta.";

        if (mostrarProceso) {
            agregarLinea(proceso, "Resumen DFS:");
            agregarLinea(proceso, "  Encontro ruta: " + (encontrado ? "si" : "no"));
            agregarLinea(proceso, "  Longitud de ruta: " + longitud);
            agregarLinea(proceso, "  Maximo de la pila: " + pila.maxCantidad());
            agregarLinea(proceso, "  Ruta: " + rutaTexto);
        }

        return new Resultado("DFS", encontrado, tiempoMs, nodosVisitados,
                longitud, pila.maxCantidad(), memoria, padre, rutaTexto, proceso.toString());
    }

    private String explicarNoApilado(int[][] mapa, int fila, int columna, boolean[][] descubierto) {
        if (!GrafoCuadricula.estaDentro(mapa, fila, columna)) {
            return "esta fuera del mapa";
        }
        if (mapa[fila][columna] == GrafoCuadricula.OBSTACULO) {
            return "es un obstaculo";
        }
        if (descubierto[fila][columna]) {
            return "ya fue descubierto";
        }
        return "no cumple una condicion de DFS";
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
