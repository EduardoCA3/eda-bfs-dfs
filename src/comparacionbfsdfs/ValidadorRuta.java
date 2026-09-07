package comparacionbfsdfs;

public class ValidadorRuta {
    private final BFS bfs;

    public ValidadorRuta() {
        bfs = new BFS();
    }

    public boolean existeRuta(int[][] mapa, int filaInicio, int columnaInicio,
            int filaDestino, int columnaDestino) {
        Resultado resultado = bfs.buscar(mapa, filaInicio, columnaInicio, filaDestino, columnaDestino);
        return resultado.encontroRuta();
    }
}
