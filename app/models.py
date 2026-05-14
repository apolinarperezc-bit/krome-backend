from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Folio(Base):
    __tablename__ = "folios"

    id              = Column(Integer, primary_key=True, index=True)  # ID interno autoincremental
    num_operacion   = Column(String(100), nullable=True)             # Folio de la tienda (manual)
    tipo            = Column(String(50), nullable=False)             # traslado / entrada / salida
    origen          = Column(String(50), nullable=True)
    destino         = Column(String(50), nullable=True)
    observaciones   = Column(Text, nullable=True)
    total_articulos = Column(Integer, default=0)
    total_piezas    = Column(Float, default=0)
    fecha_creacion  = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("FolioItem", back_populates="folio", cascade="all, delete-orphan")


class FolioItem(Base):
    __tablename__ = "folio_items"

    id          = Column(Integer, primary_key=True, index=True)
    folio_id    = Column(Integer, ForeignKey("folios.id"), nullable=False)
    sku         = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    cantidad    = Column(Float, nullable=False)

    folio = relationship("Folio", back_populates="items")


class Producto(Base):
    __tablename__ = "productos"

    sku         = Column(String(100), primary_key=True, index=True)
    descripcion = Column(Text, nullable=True)
    stock_fk01  = Column(Float, default=0)
    stock_fk02  = Column(Float, default=0)
    stock_fk03  = Column(Float, default=0)
    stock_fk08  = Column(Float, default=0)
    precio_venta = Column(Float, nullable=True)
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
