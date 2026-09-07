package comparacionbfsdfs;

import java.util.Random;

public class GeneradorEscenarios {
    private final ValidadorRuta validadorRuta;

    public GeneradorEscenarios() {
        validadorRuta = new ValidadorRuta();
    }

    public int[][] generarMapaValido(int tamano, double porcentajeObstaculos, int semillaBase) {
        int[][] mapa;
        int intento = 0;

        do {
            mapa = generarMapa(tamano, porcentajeObstaculos, semillaBase + intento);
            intento++;
        } while (!validadorRuta.existeRuta(mapa, 0, 0, tamano - 1, tamano - 1));

        return mapa;
    }

    public int[][] generarMapa(int tamano, double porcentajeObstaculos, int semilla) {
        int[][] mapa = new int[tamano][tamano];
        Random random = new Random(semilla);
        int cantidadObstaculos = (int) (tamano * tamano * porcentajeObstaculos);
        int colocados = 0;

        while (colocados < cantidadObstaculos) {
            int fila = random.nextInt(tamano);
            int columna = random.nextInt(tamano);

            if (esInicioODestino(fila, columna, tamano)) {
                continue;
            }

            if (mapa[fila][columna] == GrafoCuadricula.LIBRE) {
                mapa[fila][columna] = GrafoCuadricula.OBSTACULO;
                colocados++;
            }
        }
        return mapa;
    }

    private boolean esInicioODestino(int fila, int columna, int tamano) {
        boolean esInicio = fila == 0 && columna == 0;
        boolean esDestino = fila == tamano - 1 && columna == tamano - 1;
        return esInicio || esDestino;
    }
}
