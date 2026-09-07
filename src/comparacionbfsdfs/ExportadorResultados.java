package comparacionbfsdfs;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class ExportadorResultados {
    private static final String CARPETA_SALIDA = "salida_resultados";

    public void crearCarpetaSalida() {
        File carpeta = new File(CARPETA_SALIDA);
        if (!carpeta.exists()) {
            carpeta.mkdir();
        }
    }

    public String obtenerRutaSalidaAbsoluta() {
        File carpeta = new File(CARPETA_SALIDA);
        return carpeta.getAbsolutePath();
    }

    public PrintWriter crearEscritor(String archivo) throws IOException {
        crearCarpetaSalida();
        return new PrintWriter(new FileWriter(archivo));
    }

    public void guardarDatosEquipo() {
        try (PrintWriter pw = crearEscritor("salida_resultados/equipo_ejecucion.txt")) {
            pw.println("DATOS DEL EQUIPO");
            pw.println("Sistema operativo: " + System.getProperty("os.name"));
            pw.println("Version de Java: " + System.getProperty("java.version"));
            pw.println("Usuario: " + System.getProperty("user.name"));
        } catch (Exception e) {
            System.out.println("No se pudo guardar datos del equipo.");
        }
    }

    public void guardarMapaEjemplo(int[][] mapa, Resultado bfs, Resultado dfs, String archivo) {
        try (PrintWriter pw = crearEscritor(archivo)) {
            pw.println("MAPA DE EJEMPLO");
            pw.println("S = inicio, G = destino, # = obstaculo, . = libre");
            pw.println();
            for (int fila = 0; fila < mapa.length; fila++) {
                for (int columna = 0; columna < mapa.length; columna++) {
                    if (fila == 0 && columna == 0) {
                        pw.print("S ");
                    } else if (fila == mapa.length - 1 && columna == mapa.length - 1) {
                        pw.print("G ");
                    } else if (mapa[fila][columna] == GrafoCuadricula.OBSTACULO) {
                        pw.print("# ");
                    } else {
                        pw.print(". ");
                    }
                }
                pw.println();
            }
            pw.println();
            pw.println("BFS longitud: " + bfs.getLongitudRuta());
            pw.println("BFS ruta: " + bfs.getRutaTexto());
            pw.println();
            pw.println("DFS longitud: " + dfs.getLongitudRuta());
            pw.println("DFS ruta: " + dfs.getRutaTexto());
        } catch (Exception e) {
            System.out.println("No se pudo guardar el mapa de ejemplo.");
        }
    }

    public void guardarCsvPruebaSimple(Resultado bfs, Resultado dfs, String archivo) {
        try (PrintWriter pw = crearEscritor(archivo)) {
            pw.println("algoritmo;tiempoMs;nodosVisitados;longitudRuta;maxColaPila;memoriaAprox");
            escribirFilaPruebaSimple(pw, bfs);
            escribirFilaPruebaSimple(pw, dfs);
        } catch (Exception e) {
            System.out.println("No se pudo guardar el CSV de la prueba simple.");
        }
    }

    private void escribirFilaPruebaSimple(PrintWriter pw, Resultado resultado) {
        pw.println(resultado.getAlgoritmo() + ";"
                + resultado.getTiempoMs() + ";"
                + resultado.getNodosVisitados() + ";"
                + resultado.getLongitudRuta() + ";"
                + resultado.getMaxEstructura() + ";"
                + resultado.getMemoriaAprox());
    }

    public void guardarProcesoPruebaSimple(Resultado bfs, Resultado dfs, String archivo) {
        try (PrintWriter pw = crearEscritor(archivo)) {
            pw.println("PROCESO DETALLADO DE LA PRUEBA SIMPLE");
            pw.println();
            pw.println(bfs.getProceso());
            pw.println();
            pw.println(dfs.getProceso());
        } catch (Exception e) {
            System.out.println("No se pudo guardar el proceso detallado.");
        }
    }
}
