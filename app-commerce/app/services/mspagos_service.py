import requests
import os
import logging
from app.mapping import PagoSchema
from app.models import Pago, Producto
from tenacity import retry, stop_after_attempt, wait_random


class ClientePagosService:
    
    def __init__(self):
        self.pago = Pago()
        self.URL = os.getenv('MSPAGOS_URL', 'http://localhost:5002/api/v1/')
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def registrar_pago(self, producto: Producto, medio_pago:str ) -> None:
        self.pago.producto = producto.id
        self.pago.precio = producto.precio
        self.pago.medio_pago = medio_pago
        pago_schema = PagoSchema()
        data=pago_schema.dump(self.pago)
        logging.info(data)
        data.pop("id", None)        
        data.pop("deleted_at", None)
        r = requests.post(f'{self.URL}pagos/registrar', json=data)
        if r.status_code == 200:
            logging.info(f"Pago <- {r.json()}")
           
            self.pago = pago_schema.load( r.json() )
            logging.info(f"Pago realizado id: {self.pago.id}")
        else:
            logging.error(f"Error en el microservicio compras")
            raise BaseException("Error en el microservicio compras")

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def cancelar_pago(self) -> None:
        
        if not self.pago.id:
            logging.error("No se puede cancelar el pago sin ID")
            raise BaseException("No se puede cancelar el pago sin ID")
        
        r = requests.put(f'{self.URL}pagos/cancelar/{self.pago.id}')
        if r.status_code == 200:
            logging.warning(f"Pago eliminado ID: {self.compra.id}")
        else:
            logging.error("Error tratando de compensar Pago")
            raise BaseException("Error tratando de compensar Pago")