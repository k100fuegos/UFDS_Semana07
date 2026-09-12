from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TipoPagoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=50, min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class TipoPago(TipoPagoBase, table=True):
    __tablename__ = "tipos_pago"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)


class TipoPagoCreate(TipoPagoBase):
    pass


class TipoPagoUpdate(TipoPagoBase):
    pass
