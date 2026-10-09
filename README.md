
# CRUD de ventas — Vue 3 + Vue Router + Axios + Flask

Aplicación para Windows basada en el manual `Manual_Windows_CRUD_Vue3_Axios_Flask.pdf`.

## Requisitos
- Python 3.11 o superior
- Node.js LTS y npm
- PowerShell

## 1. Backend (PowerShell)
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
Copy-Item .env.example .env
flask --app run.py db init
flask --app run.py db migrate -m "crear clientes productos y pedidos"
flask --app run.py db upgrade
flask --app run.py run --debug
```
Si `db init` indica que la carpeta `migrations` ya existe, omite ese comando y ejecuta `db migrate` y `db upgrade`.

## 2. Frontend (otra terminal)
Desde la carpeta raíz del proyecto:
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Abre la URL que muestre Vite, normalmente http://localhost:5173.

## Funcionalidad
- CRUD de clientes, productos y pedidos.
- Cuatro rutas: inicio, clientes, productos y pedidos.
- Componentes reutilizables para botones, inputs, tablas y alertas.
- Validación en frontend y backend.
- Los pedidos descuentan existencias; solo se pueden borrar cuando están cancelados.
- No se permite borrar clientes o productos que tengan pedidos asociados.

## Estructura
- `backend/app/models.py`: modelos y relaciones SQLAlchemy.
- `backend/app/api/`: endpoints REST.
- `backend/app/extensions.py`: extensiones compartidas.
- `backend/app/__init__.py`: fábrica de Flask y configuración CORS.
- `frontend/src/api/`: cliente Axios y funciones por recurso.
- `frontend/src/components/`: componentes reutilizables.
- `frontend/src/views/`: páginas CRUD.
- `frontend/src/router/`: navegación.

Base de datos SQLite para desarrollo. Antes de producción, configurar PostgreSQL, HTTPS, autenticación y autorización. No publicar `.env`.
