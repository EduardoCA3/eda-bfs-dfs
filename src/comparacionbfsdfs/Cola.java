package comparacionbfsdfs;

public class Cola {
    private Nodo front; // cabeza de la cola
    private Nodo rear;  // final de la cola
    private int cantidad;
    private int maxCantidad;

    public Cola() {
        front = null;
        rear = null;
        cantidad = 0;
        maxCantidad = 0;
    }

    public boolean esvacia() {
        return front == null || rear == null;
    }

    public void insertar(int elemento) {
        Nodo nodo = new Nodo(elemento);
        if (front == null || rear == null) {
            front = nodo;
            rear = nodo;
        } else {
            rear.setNext(nodo);
            rear = nodo;
        }
        cantidad++;
        if (cantidad > maxCantidad) {
            maxCantidad = cantidad;
        }
    }

    public int desencolar() {
        int valor;
        if (front == null) {
            valor = -999;
        } else {
            valor = front.value();
            front = front.next();
            cantidad--;
            if (front == null) {
                rear = null;
            }
        }
        return valor;
    }

    public int cantidad() {
        return cantidad;
    }

    public int maxCantidad() {
        return maxCantidad;
    }
}
