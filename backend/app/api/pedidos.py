from flask import jsonify, request
from ..errors import error, required
from ..extensions import db
from ..models import Cliente, Pedido, Producto
from . import api_bp
ESTADOS = {"pendiente", "pagado", "enviado", "cancelado"}

@api_bp.get("/pedidos")
def listar_pedidos():
    return jsonify([x.to_dict() for x in Pedido.query.order_by(Pedido.id.desc()).all()])

@api_bp.get("/pedidos/<int:item_id>")
def obtener_pedido(item_id):
    return jsonify(db.get_or_404(Pedido, item_id).to_dict())

def validar(data):
    missing = required(data, ["cliente_id", "producto_id", "cantidad"])
    if missing: return None, error("Faltan campos obligatorios", details=missing)
    try: cliente_id, producto_id, cantidad = int(data["cliente_id"]), int(data["producto_id"]), int(data["cantidad"])
    except (TypeError, ValueError): return None, error("IDs y cantidad deben ser enteros")
    if cantidad <= 0: return None, error("La cantidad debe ser mayor que cero")
    cliente, producto = db.session.get(Cliente, cliente_id), db.session.get(Producto, producto_id)
    if not cliente or not producto: return None, error("Cliente o producto no encontrado", 404)
    if not producto.activo: return None, error("El producto está inactivo")
    if producto.stock < cantidad: return None, error("Stock insuficiente", 409)
    return {"cliente": cliente, "producto": producto, "cantidad": cantidad}, None

@api_bp.post("/pedidos")
def crear_pedido():
    data, response = validar(request.get_json(silent=True) or {})
    if response: return response
    data["producto"].stock -= data["cantidad"]
    obj = Pedido(cliente=data["cliente"], producto=data["producto"], cantidad=data["cantidad"], estado="pendiente")
    db.session.add(obj); db.session.commit()
    return jsonify(obj.to_dict()), 201

@api_bp.put("/pedidos/<int:item_id>")
def actualizar_pedido(item_id):
    obj = db.get_or_404(Pedido, item_id)
    estado = (request.get_json(silent=True) or {}).get("estado")
    if estado not in ESTADOS: return error("Estado no válido", details=sorted(ESTADOS))
    obj.estado = estado; db.session.commit()
    return jsonify(obj.to_dict())

@api_bp.delete("/pedidos/<int:item_id>")
def eliminar_pedido(item_id):
    obj = db.get_or_404(Pedido, item_id)
    if obj.estado != "cancelado": return error("Solo se pueden eliminar pedidos cancelados", 409)
    db.session.delete(obj); db.session.commit()
    return "", 204
