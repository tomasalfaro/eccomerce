from app import db
from app.models import Producto

class ProductoRepository:
    
    def save(self, producto: Producto) -> Producto:
        db.session.add(producto)
        db.session.commit()
        return producto

    def find(self, id: int) -> Producto:
        result = None
        if id is not None:
            result = db.session.query(Producto).filter(Producto.id == id, Producto.activado == True).one_or_none()
        return result