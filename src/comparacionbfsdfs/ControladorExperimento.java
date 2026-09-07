package comparacionbfsdfs;

import java.io.PrintWriter;
import java.util.Arrays;

public class ControladorExperimento {
    private final int[] tamanos = {10, 20, 50};
    private final double[] porcentajesObstaculos = {0.10, 0.20, 0.30};
    private final int repeticiones = 30;
    private final GeneradorEscenarios generadorEscenarios;
    private final ExportadorResultados exportadorResultados;
    private final EjecutorPython ejecutorPython;

    public ControladorExperimento() {
        generadorEscenarios = new GeneradorEscenarios();
        exportadorResultados = new ExportadorResultados();
        ejecutorPython = new EjecutorPython();
    }

    public void ejecutarPruebaSimple() {
        exportadorResultados.crearCarpetaSalida();

        int tamano = 10;
        double porcentaje = 0.20;
        int[][] mapa = generadorEscenarios.generarMapaValido(tamano, porcentaje, 100);

        BFS bfs = new BFS();
        DFS dfs = new DFS();

        Resultado resultadoBfs = bfs.buscar(mapa, 0, 0, tamano - 1, tamano - 1);
        Resultado resultadoDfs = dfs.buscar(mapa, 0, 0, tamano - 1, tamano - 1);
        Resultado procesoBfs = bfs.buscarConProceso(mapa, 0, 0, tamano - 1, tamano - 1);
        Resultado procesoDfs = dfs.buscarConProceso(mapa, 0, 0, tamano - 1, tamano - 1);

        System.out.println("\nPRUEBA SIMPLE 10x10 con 20% de obstaculos");
        System.out.println("Ambos algoritmos usan el mismo mapa y el mismo orden de movimiento.");
        imprimirResultado(resultadoBfs);
        imprimirResultado(resultadoDfs);

        System.out.println("\nPROCESO BFS");
        System.out.println(procesoBfs.getProceso());
        System.out.println("PROCESO DFS");
        System.out.println(procesoDfs.getProceso());

        exportadorResultados.guardarMapaEjemplo(mapa, resultadoBfs, resultadoDfs,
                "salida_resultados/mapa_ejemplo.txt");
        exportadorResultados.guardarCsvPruebaSimple(resultadoBfs, resultadoDfs,
                "salida_resultados/prueba_simple_resultados.csv");
        exportadorResultados.guardarProcesoPruebaSimple(procesoBfs, procesoDfs,
                "salida_resultados/proceso_prueba_simple.txt");

        System.out.println("\nGenerando graficos de la opcion 1...");
        ejecutorPython.ejecutarScript("scripts\\generar_animacion_grafos.py");
        ejecutorPython.ejecutarScript("scripts\\generar_grafico_prueba_simple.py");

        System.out.println("\nArchivos generados:");
        System.out.println("- salida_resultados/mapa_ejemplo.txt");
        System.out.println("- salida_resultados/prueba_simple_resultados.csv");
        System.out.println("- salida_resultados/proceso_prueba_simple.txt");
        System.out.println("- salida_resultados/animacion_grafos.html");
        System.out.println("- salida_resultados/dashboard_prueba_simple.html");
        System.out.println("\nCarpeta exacta donde se guardaron:");
        System.out.println(exportadorResultados.obtenerRutaSalidaAbsoluta());
    }

    public void ejecutarComparacionCompleta() {
        exportadorResultados.crearCarpetaSalida();

        try (PrintWriter detalle = exportadorResultados.crearEscritor("salida_resultados/detalle_resultados.csv");
                PrintWriter resumen = exportadorResultados.crearEscritor("salida_resultados/resumen_resultados.csv");
                PrintWriter proceso = exportadorResultados.crearEscritor("salida_resultados/proceso_comparacion.txt");
                PrintWriter mapasAnimacion = exportadorResultados.crearEscritor("salida_resultados/mapas_animacion_opcion2.txt")) {

            detalle.println("tamano;obstaculos;repeticion;algoritmo;tiempoMs;nodosVisitados;longitudRuta;maxColaPila;memoriaAprox");
            resumen.println("tamano;obstaculos;algoritmo;promTiempo;medianaTiempo;desvTiempo;promVisitados;promRuta;promMemoria");
            mapasAnimacion.println("MAPAS REPRESENTATIVOS PARA ANIMACION DE LA OPCION 2");
            mapasAnimacion.println("Cada escenario guarda la primera repeticion generada.");
            mapasAnimacion.println();

            escribirInicioProcesoGeneral(proceso);

            for (int tamano : tamanos) {
                for (double porcentaje : porcentajesObstaculos) {
                    ejecutarEscenario(tamano, porcentaje, detalle, resumen, proceso, mapasAnimacion);
                }
            }

            exportadorResultados.guardarDatosEquipo();

            detalle.flush();
            resumen.flush();
            proceso.flush();
            mapasAnimacion.flush();

            System.out.println("\nGenerando graficos de la opcion 2...");
            ejecutorPython.ejecutarScript("scripts\\generar_graficos.py");
            ejecutorPython.ejecutarScript("scripts\\generar_animacion_opcion2.py");

            System.out.println("\nListo. Archivos generados en la carpeta salida_resultados.");
            System.out.println("- detalle_resultados.csv");
            System.out.println("- resumen_resultados.csv");
            System.out.println("- proceso_comparacion.txt");
            System.out.println("- mapas_animacion_opcion2.txt");
            System.out.println("- equipo_ejecucion.txt");
            System.out.println("- dashboard_resultados.html");
            System.out.println("- animacion_opcion2.html");
            System.out.println("- graficos/*.svg");
            System.out.println("\nCarpeta exacta donde se guardaron:");
            System.out.println(exportadorResultados.obtenerRutaSalidaAbsoluta());

        } catch (Exception e) {
            System.out.println("Error al guardar resultados: " + e.getMessage());
        }
    }

    private void escribirInicioProcesoGeneral(PrintWriter proceso) {
        proceso.println("PROCESO GENERAL DE COMPARACION");
        proceso.println("1. Se define el tamano de la cuadricula: 10x10, 20x20 y 50x50.");
        proceso.println("2. Se define el porcentaje de obstaculos: 10%, 20% y 30%.");
        proceso.println("3. Para cada escenario se genera un mapa valido con ruta disponible.");
        proceso.println("4. BFS y DFS se ejecutan sobre el mismo mapa para comparar en igualdad de condiciones.");
        proceso.println("5. Se registran tiempo, nodos visitados, longitud de ruta y memoria aproximada.");
        proceso.println("6. Cada escenario se repite 30 veces y luego se calcula promedio, mediana y desviacion.");
        proceso.println();
    }

    private void ejecutarEscenario(int tamano, double porcentaje, PrintWriter detalle,
            PrintWriter resumen, PrintWriter proceso, PrintWriter mapasAnimacion) {
        double[] tiempoBfs = new double[repeticiones];
        double[] tiempoDfs = new double[repeticiones];
        double[] visitadosBfs = new double[repeticiones];
        double[] visitadosDfs = new double[repeticiones];
        double[] rutaBfs = new double[repeticiones];
        double[] rutaDfs = new double[repeticiones];
        double[] memoriaBfs = new double[repeticiones];
        double[] memoriaDfs = new double[repeticiones];

        BFS bfs = new BFS();
        DFS dfs = new DFS();

        proceso.println("ESCENARIO: " + tamano + "x" + tamano + " con "
                + (int) (porcentaje * 100) + "% de obstaculos");

        for (int repeticion = 0; repeticion < repeticiones; repeticion++) {
            int semillaBase = 1000 + tamano * 10 + repeticion;
            int[][] mapa = generadorEscenarios.generarMapaValido(tamano, porcentaje, semillaBase);
            Resultado rb = bfs.buscar(mapa, 0, 0, tamano - 1, tamano - 1);
            Resultado rd = dfs.buscar(mapa, 0, 0, tamano - 1, tamano - 1);

            if (repeticion == 0) {
                escribirMapaAnimacion(mapasAnimacion, tamano, porcentaje, repeticion + 1, mapa);
            }

            tiempoBfs[repeticion] = rb.getTiempoMs();
            tiempoDfs[repeticion] = rd.getTiempoMs();
            visitadosBfs[repeticion] = rb.getNodosVisitados();
            visitadosDfs[repeticion] = rd.getNodosVisitados();
            rutaBfs[repeticion] = rb.getLongitudRuta();
            rutaDfs[repeticion] = rd.getLongitudRuta();
            memoriaBfs[repeticion] = rb.getMemoriaAprox();
            memoriaDfs[repeticion] = rd.getMemoriaAprox();

            escribirDetalle(detalle, tamano, porcentaje, repeticion + 1, rb);
            escribirDetalle(detalle, tamano, porcentaje, repeticion + 1, rd);

            proceso.println("  Repeticion " + (repeticion + 1)
                    + ": mapa valido generado con semilla base " + semillaBase + ".");
            proceso.println("    BFS -> visitados=" + rb.getNodosVisitados()
                    + ", ruta=" + rb.getLongitudRuta()
                    + ", maxCola=" + rb.getMaxEstructura() + ".");
            proceso.println("    DFS -> visitados=" + rd.getNodosVisitados()
                    + ", ruta=" + rd.getLongitudRuta()
                    + ", maxPila=" + rd.getMaxEstructura() + ".");
        }

        escribirResumen(resumen, tamano, porcentaje, "BFS", tiempoBfs, visitadosBfs,
                rutaBfs, memoriaBfs);
        escribirResumen(resumen, tamano, porcentaje, "DFS", tiempoDfs, visitadosDfs,
                rutaDfs, memoriaDfs);

        proceso.println("  Se escriben promedios, mediana y desviacion del escenario.");
        proceso.println();

        System.out.println("Escenario " + tamano + "x" + tamano + " con "
                + (int) (porcentaje * 100) + "% listo.");
    }

    private void escribirMapaAnimacion(PrintWriter mapasAnimacion, int tamano,
            double porcentaje, int repeticion, int[][] mapa) {
        mapasAnimacion.println("ESCENARIO;" + tamano + ";" + (int) (porcentaje * 100)
                + ";" + repeticion);
        for (int fila = 0; fila < mapa.length; fila++) {
            for (int columna = 0; columna < mapa.length; columna++) {
                if (fila == 0 && columna == 0) {
                    mapasAnimacion.print("S");
                } else if (fila == mapa.length - 1 && columna == mapa.length - 1) {
                    mapasAnimacion.print("G");
                } else if (mapa[fila][columna] == GrafoCuadricula.OBSTACULO) {
                    mapasAnimacion.print("#");
                } else {
                    mapasAnimacion.print(".");
                }
                if (columna < mapa.length - 1) {
                    mapasAnimacion.print(" ");
                }
            }
            mapasAnimacion.println();
        }
        mapasAnimacion.println("FIN_ESCENARIO");
        mapasAnimacion.println();
    }

    private void escribirDetalle(PrintWriter detalle, int tamano, double porcentaje,
            int repeticion, Resultado resultado) {
        detalle.println(tamano + ";" + (int) (porcentaje * 100) + "%;" + repeticion + ";"
                + resultado.getAlgoritmo() + ";"
                + resultado.getTiempoMs() + ";"
                + resultado.getNodosVisitados() + ";"
                + resultado.getLongitudRuta() + ";"
                + resultado.getMaxEstructura() + ";"
                + resultado.getMemoriaAprox());
    }

    private void escribirResumen(PrintWriter resumen, int tamano, double porcentaje,
            String algoritmo, double[] tiempos, double[] visitados,
            double[] rutas, double[] memorias) {
        resumen.println(tamano + ";" + (int) (porcentaje * 100) + "%;" + algoritmo + ";"
                + promedio(tiempos) + ";"
                + mediana(tiempos) + ";"
                + desviacion(tiempos) + ";"
                + promedio(visitados) + ";"
                + promedio(rutas) + ";"
                + promedio(memorias));
    }

    private void imprimirResultado(Resultado resultado) {
        System.out.println(resultado.getAlgoritmo()
                + " -> Tiempo: " + resultado.getTiempoMs() + " ms"
                + " | Visitados: " + resultado.getNodosVisitados()
                + " | Ruta: " + resultado.getLongitudRuta()
                + " | Max estructura: " + resultado.getMaxEstructura()
                + " | Memoria aprox: " + resultado.getMemoriaAprox());
        System.out.println("Ruta " + resultado.getAlgoritmo() + ": " + resultado.getRutaTexto());
    }

    private double promedio(double[] datos) {
        double suma = 0;
        for (double dato : datos) {
            suma += dato;
        }
        return suma / datos.length;
    }

    private double mediana(double[] datos) {
        double[] copia = datos.clone();
        Arrays.sort(copia);
        int mitad = copia.length / 2;
        if (copia.length % 2 == 0) {
            return (copia[mitad - 1] + copia[mitad]) / 2.0;
        }
        return copia[mitad];
    }

    private double desviacion(double[] datos) {
        double prom = promedio(datos);
        double suma = 0;
        for (double dato : datos) {
            suma += Math.pow(dato - prom, 2);
        }
        return Math.sqrt(suma / datos.length);
    }
}
