package comparacionbfsdfs;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        ControladorExperimento controlador = new ControladorExperimento();
        int op;

        System.out.println("============================================");
        System.out.println(" COMPARACION DE ALGORITMOS BFS Y DFS");
        System.out.println("============================================");
        System.out.println("1. Ejecutar prueba simple 10x10");
        System.out.println("2. Ejecutar comparacion completa");
        System.out.println("0. Salir");
        System.out.print("Ingrese opcion: ");
        op = entrada.nextInt();

        switch (op) {
            case 1:
                controlador.ejecutarPruebaSimple();
                break;
            case 2:
                controlador.ejecutarComparacionCompleta();
                break;
            case 0:
                System.out.println("Programa finalizado.");
                break;
            default:
                System.out.println("Opcion invalida.");
                break;
        }
    }
}
