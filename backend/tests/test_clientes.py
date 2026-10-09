def test_crear_y_listar_cliente(client):
    response = client.post("/api/clientes", json={"nombre": "Cliente prueba", "correo": "prueba@example.com"})
    assert response.status_code == 201
    assert response.json["nombre"] == "Cliente prueba"
    assert client.get("/api/clientes").status_code == 200

def test_correo_duplicado(client):
    payload = {"nombre": "Uno", "correo": "igual@example.com"}
    assert client.post("/api/clientes", json=payload).status_code == 201
    assert client.post("/api/clientes", json=payload).status_code == 409
