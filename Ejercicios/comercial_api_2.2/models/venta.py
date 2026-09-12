from decimal import Decimal
from datetime import datetime
from sqlmodel import SQLModel, Field


class VentaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.utcnow)
    id_cliente: int = Field(nullable=False, foreign_key="clientes.id")
    id_usuario: int = Field(nullable=False, foreign_key="usuarios.id")
    id_tipo_pago: int = Field(nullable=False, foreign_key="tipos_pago.id")
    subtotal: Decimal = Field(nullable=False, ge=0)
    iva: Decimal = Field(nullable=False, ge=0)
    total: Decimal = Field(nullable=False, ge=0)


class Venta(VentaBase, table=True):
    __tablename__ = "ventas"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)


class VentaCreate(VentaBase):
    pass


class VentaUpdate(VentaBase):
    pass
