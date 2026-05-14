from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── ITEMS ────────────────────────────────────────────────────────────────────

class FolioItemCreate(BaseModel):
    sku: str
    descripcion: Optional[str] = None
    cantidad: float

class FolioItemOut(FolioItemCreate):
    id: int
    folio_id: int
    class Config:
        from_attributes = True


# ── FOLIOS ───────────────────────────────────────────────────────────────────

class FolioCreate(BaseModel):
    num_operacion: Optional[str] = None
    tipo: str
    origen: Optional[str] = None
    destino: Optional[str] = None
    observaciones: Optional[str] = None
    items: list[FolioItemCreate]

class FolioOut(BaseModel):
    id: int
    num_operacion: Optional[str]
    tipo: str
    origen: Optional[str]
    destino: Optional[str]
    observaciones: Optional[str]
    total_articulos: int
    total_piezas: float
    fecha_creacion: datetime
    items: list[FolioItemOut]
    class Config:
        from_attributes = True


# ── PRODUCTOS ────────────────────────────────────────────────────────────────

class ProductoCreate(BaseModel):
    sku: str
    descripcion: Optional[str] = None
    stock_fk01: float = 0
    stock_fk02: float = 0
    stock_fk03: float = 0
    stock_fk08: float = 0
    precio_venta: Optional[float] = None

class ProductoOut(ProductoCreate):
    updated_at: datetime
    class Config:
        from_attributes = True
