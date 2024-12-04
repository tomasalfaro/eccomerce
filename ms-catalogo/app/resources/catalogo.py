from flask import Blueprint
from flask import request
from marshmallow import ValidationError
from app.mapping import ProductoSchema
from app.services import ProductoService

catalogo_bp = Blueprint('catalogo', __name__)
producto_schema = ProductoSchema()
producto_service = ProductoService()

@catalogo_bp.route('/catalogo/productos/<int:id>', methods=['GET'])
def get_producto(id: int):
    result = producto_schema.dump(producto_service.find(id))
    if result:
        status_code = 200 
    else:
        status_code = 404
    return result, status_code

@catalogo_bp.route('/catalogo/guardar', methods=['POST'])
def guardar():
    data = request.json
    producto = producto_schema.load(data)
    result = producto_schema.dump(producto_service.save(producto))
    if result:  
        status_code = 200 
    else:
        status_code = 404
    return result, status_code