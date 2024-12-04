import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check, sleep } from 'k6';

// Métrica personalizada para rastrear el estado de las respuestas
const statusTrend = new Trend('status_codes');

export const options = {
    stages: [
        { duration: '7s', target: 20 }, // Escalar hasta 50 usuarios simultáneos en 10 segundos
        { duration: '20s', target: 20 }, // Mantener 20 usuarios simultáneos durante 20 segundos
        { duration: '7s', target: 0 },  // Reducir a 0 usuarios simultáneos en 10 segundos
    ],
};

export default function () {
    const BASE_URL = 'http://localhost:5000/api/v1/commerce/consultar/catalogo'; // URL base del servidor de desarrollo

    // Simulamos un producto aleatorio con ID entre 1 y 3
    const numeros = [1, 2, 3,4];
    const producto_id = numeros[Math.floor(Math.random() * numeros.length)];
    

    const res = http.get(`${BASE_URL}/${producto_id}`);

    // Registrar métricas de los estados HTTP
    statusTrend.add(res.status);

    // Validaciones básicas
    check(res, {
        'status is 200': (r) => r.status === 200,
        'status is 404': (r) => r.status === 404,
    });

    sleep(1); // Simular espera de 1 segundo entre solicitudes
}