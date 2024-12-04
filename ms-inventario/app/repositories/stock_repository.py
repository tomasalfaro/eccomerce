from app import db
from typing import List
from app.models import Stock
import logging
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy import func, case

class StockRepository:

    def save(self, stock: Stock) -> Stock:
        db.session.add(stock)
        db.session.commit()
        return stock
    
    def cuantity(self, producto_id: int) -> float:
        entradas = db.session.query(
            func.sum(case((Stock.entrada_salida == 1, Stock.cantidad), else_=0))
        ).filter(Stock.producto == producto_id).scalar() or 0

        salidas = db.session.query(
            func.sum(case((Stock.entrada_salida == 2, Stock.cantidad), else_=0))
        ).filter(Stock.producto == producto_id).scalar() or 0

        return entradas - salidas
                   






# 50 compras por segundo
#1)test de carga con k6 de servidor de desarrollo
# docker build -f ./Dockerfile.gunicorn -t app-commerce:gunicorn
# test de carga con k6 de servidor de gunicorn
# docker build -f ./Dockerfile -t app-commerce:uwsgi
# test de carga con k6 de servidor de uwsgi
# test de carga aplicando traefik  con balanceo de carga y escalado horizontal



#mkcert