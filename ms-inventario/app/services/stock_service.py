from app import db
from app.models import Stock
from app.repositories import StockRepository
from datetime import datetime
from app import cache
from sqlalchemy import func, case
import threading

repository = StockRepository()
class StockService:
    
    def retirar(self, stock: Stock) -> Stock:
        # Calcular stock disponible
        stock_disponible = db.session.query(
            func.sum(case((Stock.entrada_salida == 1, Stock.cantidad), else_=0)) -
            func.sum(case((Stock.entrada_salida == 2, Stock.cantidad), else_=0))
        ).filter(Stock.producto == stock.producto).scalar() or 0

        if stock.cantidad > stock_disponible:
            raise ValueError("Stock insuficiente")
        
        # Continuar con la transacción de salida
        stock.fecha_transaccion = stock.fecha_transaccion or datetime.now()
        stock.entrada_salida = 2  # Salida de Producto
        result = repository.save(stock)
        cache.set(f'stock_{stock.id}', result, timeout=60)
        return result

    def ingresar(self, stock: Stock) -> Stock:
        result = None
        if stock is not None:
            stock.fecha_transaccion = stock.fecha_transaccion if stock.fecha_transaccion is not None else datetime.now()
            stock.entrada_salida = 1 # Entrada de Producto
            result = repository.save(stock)
            cache.set(f'stock_{stock.id}', result, timeout=60)
        return result
    
    def consultar_cantidad(self, producto_id: int) ->float:
        return repository.cuantity(producto_id)


