from marshmallow import fields, Schema, post_load
from app.models import Producto

class ProductoSchema(Schema):
    id = fields.Integer(required=True)
    nombre = fields.String(required=True)
    precio = fields.Float(required=True)
    activado = fields.Boolean(required=True)

    @post_load
    def make_producto(self, data, **kwargs):
        return Producto(**data)