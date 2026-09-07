package comparacionbfsdfs;

public class Nodo {
    private int valor;
    private Nodo next;

    public Nodo(int valor) {
        this.valor = valor;
        this.next = null;
    }

    public int value() {
        return valor;
    }

    public Nodo next() {
        return next;
    }

    public void setNext(Nodo node) {
        this.next = node;
    }
}
