from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from ..errors import error, required
from ..extensions import db
from ..models import Cliente
from . import api_bp

@api_bp.get("/clientes")
def listar_clientes():
    return jsonify([x.to_dict() for x in Cliente.query.order_by(Cliente.id.desc()).all()])

@api_bp.get("/clientes/<int:item_id>")
def obtener_cliente(item_id):
    return jsonify(db.get_or_404(Cliente, item_id).to_dict())

def validar(data):
    missing = required(data, ["nombre", "correo"])
    if missing: return None, error("Faltan campos obligatorios", details=missing)
    nombre, correo = str(data["nombre"]).strip(), str(data["correo"]).strip().lower()
    if not nombre: return None, error("El nombre es obligatorio")
    if "@" not in correo or "." not in correo.rsplit("@", 1)[-1]: return None, error("Correo electrónico no válido")
    return {"nombre": nombre, "correo": correo, "telefono": str(data.get("telefono") or "").strip()}, None

@api_bp.post("/clientes")
def crear_cliente():
    values, response = validar(request.get_json(silent=True) or {})
    if response: return response
    obj = Cliente(**values); db.session.add(obj)
    try: db.session.commit()
    except IntegrityError:
        db.session.rollback(); return error("El correo ya está registrado", 409)
    return jsonify(obj.to_dict()), 201

@api_bp.put("/clientes/<int:item_id>")
def actualizar_cliente(item_id):
    obj = db.get_or_404(Cliente, item_id)
    values, response = validar(request.get_json(silent=True) or {})
    if response: return response
    for key, value in values.items(): setattr(obj, key, value)
    try: db.session.commit()
    except IntegrityError:
        db.session.rollback(); return error("El correo ya está registrado", 409)
    return jsonify(obj.to_dict())

@api_bp.delete("/clientes/<int:item_id>")
def eliminar_cliente(item_id):
    obj = db.get_or_404(Cliente, item_id)
    if obj.pedidos: return error("No se puede eliminar un cliente con pedidos", 409)
    db.session.delete(obj); db.session.commit()
    return "", 204
