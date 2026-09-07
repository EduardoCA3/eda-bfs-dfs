package comparacionbfsdfs;

public class Resultado {
    private final String algoritmo;
    private final boolean encontroRuta;
    private final double tiempoMs;
    private final int nodosVisitados;
    private final int longitudRuta;
    private final int maxEstructura;
    private final int memoriaAprox;
    private final int[][] padre;
    private final String rutaTexto;
    private final String proceso;

    public Resultado(String algoritmo, boolean encontroRuta, double tiempoMs,
            int nodosVisitados, int longitudRuta, int maxEstructura,
            int memoriaAprox, int[][] padre) {
        this(algoritmo, encontroRuta, tiempoMs, nodosVisitados, longitudRuta,
                maxEstructura, memoriaAprox, padre, "", "");
    }

    public Resultado(String algoritmo, boolean encontroRuta, double tiempoMs,
            int nodosVisitados, int longitudRuta, int maxEstructura,
            int memoriaAprox, int[][] padre, String rutaTexto, String proceso) {
        this.algoritmo = algoritmo;
        this.encontroRuta = encontroRuta;
        this.tiempoMs = tiempoMs;
        this.nodosVisitados = nodosVisitados;
        this.longitudRuta = longitudRuta;
        this.maxEstructura = maxEstructura;
        this.memoriaAprox = memoriaAprox;
        this.padre = padre;
        this.rutaTexto = rutaTexto;
        this.proceso = proceso;
    }

    public String getAlgoritmo() {
        return algoritmo;
    }

    public boolean encontroRuta() {
        return encontroRuta;
    }

    public double getTiempoMs() {
        return tiempoMs;
    }

    public int getNodosVisitados() {
        return nodosVisitados;
    }

    public int getLongitudRuta() {
        return longitudRuta;
    }

    public int getMaxEstructura() {
        return maxEstructura;
    }

    public int getMemoriaAprox() {
        return memoriaAprox;
    }

    public int[][] getPadre() {
        return padre;
    }

    public String getRutaTexto() {
        return rutaTexto;
    }

    public String getProceso() {
        return proceso;
    }
}
