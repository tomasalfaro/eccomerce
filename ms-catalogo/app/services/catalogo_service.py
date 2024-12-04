from app.models import Producto
from app.repositories import ProductoRepository
from app import cache

repository = ProductoRepository()
class ProductoService:
    
    def find(self, id: int) -> Producto:
        result = None
        if id is not None:
            result = cache.get(f"producto_{id}")
            if result is None:
                result = repository.find(id)
                cache.set(f"producto_{id}", result, 50)
        return result
    
    def save(self, producto: Producto) -> Producto:
        # Guardar el producto en el repositorio
        producto = repository.save(producto)
        cache.set(f"producto_{producto.id}", producto, timeout=30)
        return producto