from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ClienteBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=2)
    apellido: str = Field(nullable=False, max_length=100, min_length=2)
    telefono: str = Field(nullable=False, max_length=20)
    email: str = Field(nullable=False, max_length=150)
    direccion: Optional[str] = Field(default=None, max_length=255)


class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    pass
