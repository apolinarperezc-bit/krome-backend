# Krome Backend — API de Traslados

Backend FastAPI + PostgreSQL para el sistema de digitalización de Ferreterías Krome.

---

## Deploy en Railway (paso a paso)

### 1. Subir a GitHub

```bash
git init
git add .
git commit -m "feat: krome backend inicial"
git remote add origin https://github.com/TU_USUARIO/krome-backend.git
git push -u origin main
```

### 2. Crear proyecto en Railway

1. Entrar a [railway.app](https://railway.app) → **New Project**
2. Elegir **Deploy from GitHub repo**
3. Seleccionar el repo `krome-backend`
4. Railway detecta el `Procfile` y arranca automáticamente

### 3. Agregar PostgreSQL

1. Dentro del proyecto en Railway → **+ New** → **Database** → **PostgreSQL**
2. Railway conecta la BD automáticamente vía la variable `DATABASE_URL`
3. No se necesita configurar nada más

### 4. Verificar que funciona

Una vez deployado, Railway asigna una URL pública tipo:
```
https://krome-backend-production.up.railway.app
```

Probar:
```
GET  /health          → {"status": "ok"}
GET  /docs            → Documentación interactiva (Swagger)
```

---

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/folios` | Guardar un traslado/entrada/salida |
| GET | `/folios` | Listar folios (filtrar por tienda o tipo) |
| GET | `/folios/{id}` | Obtener folio por ID interno |
| GET | `/productos/{sku}` | Consultar producto por SKU |
| POST | `/productos/importar` | Importar catálogo desde Odoo |

### Ejemplo — guardar un folio

```json
POST /folios
{
  "num_operacion": "215",
  "tipo": "traslado",
  "origen": "Fk03",
  "destino": "Fk02",
  "observaciones": "",
  "items": [
    { "sku": "210046", "descripcion": "Garrucha P/Pozo No. 4", "cantidad": 1 },
    { "sku": "7506240657101", "descripcion": "Metro cable THHW-LS 10 AWG negro", "cantidad": 50 }
  ]
}
```

Respuesta:
```json
{
  "id": 1,
  "num_operacion": "215",
  "tipo": "traslado",
  "origen": "Fk03",
  "destino": "Fk02",
  "total_articulos": 2,
  "total_piezas": 51,
  "fecha_creacion": "2026-05-13T10:30:00Z",
  "items": [...]
}
```

---

## Desarrollo local

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Sin PostgreSQL local: usa SQLite automáticamente
uvicorn app.main:app --reload
```

Abrir: http://localhost:8000/docs
