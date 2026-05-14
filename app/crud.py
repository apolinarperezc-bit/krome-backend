from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from . import models, schemas


# ── FOLIOS ───────────────────────────────────────────────────────────────────

def crear_folio(db: Session, data: schemas.FolioCreate) -> models.Folio:
    total_piezas = sum(i.cantidad for i in data.items)
    folio = models.Folio(
        num_operacion   = data.num_operacion,
        tipo            = data.tipo,
        origen          = data.origen,
        destino         = data.destino,
        observaciones   = data.observaciones,
        total_articulos = len(data.items),
        total_piezas    = total_piezas,
    )
    db.add(folio)
    db.flush()  # obtener folio.id antes de commit

    for item_data in data.items:
        item = models.FolioItem(
            folio_id    = folio.id,
            sku         = item_data.sku,
            descripcion = item_data.descripcion,
            cantidad    = item_data.cantidad,
        )
        db.add(item)

    db.commit()
    db.refresh(folio)
    return folio


def listar_folios(
    db: Session,
    tienda: Optional[str] = None,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Folio]:
    q = db.query(models.Folio)
    if tienda:
        q = q.filter(or_(models.Folio.origen == tienda, models.Folio.destino == tienda))
    if tipo:
        q = q.filter(models.Folio.tipo == tipo)
    return q.order_by(models.Folio.fecha_creacion.desc()).offset(skip).limit(limit).all()


def obtener_folio(db: Session, folio_id: int) -> models.Folio | None:
    return db.query(models.Folio).filter(models.Folio.id == folio_id).first()


# ── PRODUCTOS ────────────────────────────────────────────────────────────────

def obtener_producto(db: Session, sku: str) -> models.Producto | None:
    return db.query(models.Producto).filter(models.Producto.sku == sku).first()


def importar_productos(db: Session, productos: list[schemas.ProductoCreate]) -> int:
    count = 0
    for p in productos:
        existing = db.query(models.Producto).filter(models.Producto.sku == p.sku).first()
        if existing:
            for field, val in p.model_dump().items():
                setattr(existing, field, val)
        else:
            db.add(models.Producto(**p.model_dump()))
        count += 1
    db.commit()
    return count
