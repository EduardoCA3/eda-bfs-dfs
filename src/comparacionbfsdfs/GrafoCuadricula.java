package comparacionbfsdfs;

public class GrafoCuadricula {
    public static final int LIBRE = 0;
    public static final int OBSTACULO = 1;

    public static final int[] CAMBIO_FILA = {-1, 0, 1, 0};
    public static final int[] CAMBIO_COLUMNA = {0, 1, 0, -1};
    public static final String[] DIRECCIONES = {"arriba", "derecha", "abajo", "izquierda"};

    private GrafoCuadricula() {
    }

    public static boolean estaDentro(int[][] mapa, int fila, int columna) {
        return fila >= 0 && columna >= 0 && fila < mapa.length && columna < mapa.length;
    }

    public static boolean esCeldaLibre(int[][] mapa, int fila, int columna) {
        return estaDentro(mapa, fila, columna) && mapa[fila][columna] == LIBRE;
    }

    public static int convertirAId(int fila, int columna, int tamano) {
        return fila * tamano + columna;
    }

    public static int obtenerFila(int id, int tamano) {
        return id / tamano;
    }

    public static int obtenerColumna(int id, int tamano) {
        return id % tamano;
    }

    public static String posicion(int fila, int columna) {
        return "(" + fila + "," + columna + ")";
    }
}
