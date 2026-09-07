package comparacionbfsdfs;

public class Pila {
    private Nodo top;
    private int cantidad;
    private int maxCantidad;

    public Pila() {
        top = null;
        cantidad = 0;
        maxCantidad = 0;
    }

    public boolean esvacia() {
        return top == null;
    }

    public void push(int elemento) {
        Nodo nuevo = new Nodo(elemento);
        nuevo.setNext(top);
        top = nuevo;
        cantidad++;
        if (cantidad > maxCantidad) {
            maxCantidad = cantidad;
        }
    }

    public int pop() {
        int valor;
        if (top == null) {
            valor = -999;
        } else {
            valor = top.value();
            top = top.next();
            cantidad--;
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
