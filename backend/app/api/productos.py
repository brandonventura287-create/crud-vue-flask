from decimal import Decimal, InvalidOperation
from flask import jsonify, request
from ..errors import error, required
from ..extensions import db
from ..models import Producto
from . import api_bp

def validar(data):
    missing = required(data, ["nombre", "precio", "stock"])
    if missing: return None, error("Faltan campos obligatorios", details=missing)
    try:
        precio, stock = Decimal(str(data["precio"])), int(data["stock"])
    except (InvalidOperation, TypeError, ValueError):
        return None, error("Precio o stock no válidos")
    nombre = str(data["nombre"]).strip()
    if not nombre: return None, error("El nombre es obligatorio")
    if not precio.is_finite() or precio < 0 or stock < 0: return None, error("Precio y stock deben ser mayores o iguales a cero")
    return {"nombre": nombre, "descripcion": str(data.get("descripcion") or "").strip(),
            "precio": precio, "stock": stock, "activo": bool(data.get("activo", True))}, None

@api_bp.get("/productos")
def listar_productos():
    return jsonify([x.to_dict() for x in Producto.query.order_by(Producto.id.desc()).all()])

@api_bp.get("/productos/<int:item_id>")
def obtener_producto(item_id):
    return jsonify(db.get_or_404(Producto, item_id).to_dict())

@api_bp.post("/productos")
def crear_producto():
    values, response = validar(request.get_json(silent=True) or {})
    if response: return response
    obj = Producto(**values); db.session.add(obj); db.session.commit()
    return jsonify(obj.to_dict()), 201

@api_bp.put("/productos/<int:item_id>")
def actualizar_producto(item_id):
    obj = db.get_or_404(Producto, item_id)
    values, response = validar(request.get_json(silent=True) or {})
    if response: return response
    for key, value in values.items(): setattr(obj, key, value)
    db.session.commit()
    return jsonify(obj.to_dict())

@api_bp.delete("/productos/<int:item_id>")
def eliminar_producto(item_id):
    obj = db.get_or_404(Producto, item_id)
    if obj.pedidos: return error("No se puede eliminar un producto con pedidos", 409)
    db.session.delete(obj); db.session.commit()
    return "", 204
