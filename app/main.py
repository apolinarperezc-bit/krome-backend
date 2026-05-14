from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, crud
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ferreterías Krome API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción limitar al dominio del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── FOLIOS ──────────────────────────────────────────────────────────────────

@app.post("/folios", response_model=schemas.FolioOut)
def crear_folio(folio: schemas.FolioCreate, db: Session = Depends(get_db)):
    return crud.crear_folio(db, folio)

@app.get("/folios", response_model=list[schemas.FolioOut])
def listar_folios(
    tienda: Optional[str] = None,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.listar_folios(db, tienda=tienda, tipo=tipo, skip=skip, limit=limit)

@app.get("/folios/{folio_id}", response_model=schemas.FolioOut)
def obtener_folio(folio_id: int, db: Session = Depends(get_db)):
    folio = crud.obtener_folio(db, folio_id)
    if not folio:
        raise HTTPException(status_code=404, detail="Folio no encontrado")
    return folio


# ── PRODUCTOS ────────────────────────────────────────────────────────────────

@app.get("/productos/{sku}", response_model=schemas.ProductoOut)
def obtener_producto(sku: str, db: Session = Depends(get_db)):
    prod = crud.obtener_producto(db, sku)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@app.post("/productos/importar")
def importar_productos(productos: list[schemas.ProductoCreate], db: Session = Depends(get_db)):
    count = crud.importar_productos(db, productos)
    return {"importados": count}


# ── HEALTH ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}
