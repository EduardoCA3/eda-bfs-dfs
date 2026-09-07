package comparacionbfsdfs;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class EjecutorPython {

    public boolean ejecutarScript(String script) {
        boolean ejecutado = ejecutarConComando("python", script);
        if (!ejecutado) {
            ejecutado = ejecutarConComando("py", script);
        }
        if (!ejecutado) {
            System.out.println("No se pudo ejecutar Python automaticamente.");
            System.out.println("Puedes generarlo manualmente con:");
            System.out.println("python " + script);
        }
        return ejecutado;
    }

    private boolean ejecutarConComando(String comandoPython, String script) {
        try {
            ProcessBuilder pb = new ProcessBuilder(comandoPython, script);
            pb.redirectErrorStream(true);
            Process proceso = pb.start();

            try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(proceso.getInputStream()))) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    System.out.println(linea);
                }
            }

            int codigoSalida = proceso.waitFor();
            return codigoSalida == 0;
        } catch (Exception e) {
            return false;
        }
    }
}
