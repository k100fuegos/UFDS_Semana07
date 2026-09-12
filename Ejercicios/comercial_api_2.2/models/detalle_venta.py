from decimal import Decimal
from datetime import datetime
from sqlmodel import SQLModel, Field


class DetalleVentaBase(SQLModel):
    id_venta: int = Field(nullable=False, foreign_key="ventas.id")
    id_producto: int = Field(nullable=False, foreign_key="productos.id")
    cantidad: int = Field(nullable=False, ge=1)
    precio_unitario: Decimal = Field(nullable=False, gt=0)
    subtotal: Decimal = Field(nullable=False, ge=0)


class DetalleVenta(DetalleVentaBase, table=True):
    __tablename__ = "detalle_ventas"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)


class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaUpdate(DetalleVentaBase):
    pass
