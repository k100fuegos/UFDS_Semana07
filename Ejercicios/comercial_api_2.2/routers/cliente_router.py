from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.cliente import Cliente, ClienteCreate, ClienteUpdate
from config.security_Dependencia import Token_Dependencia

router = APIRouter()


@router.get("/clientes", response_model=list[Cliente], status_code=status.HTTP_200_OK)
async def get_clientes(session: SessionDeDependencia,
                       offset: int = Query(0, ge=0),
                       limit: int = Query(20, ge=1)):
    consulta = select(Cliente).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
async def get_cliente(id: int, session: SessionDeDependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return resultado


@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente(datos_cliente: ClienteCreate, session: SessionDeDependencia):
    cliente_nuevo = Cliente(
        nombre=datos_cliente.nombre,
        apellido=datos_cliente.apellido,
        telefono=datos_cliente.telefono,
        email=datos_cliente.email,
        direccion=datos_cliente.direccion,
    )
    session.add(cliente_nuevo)
    session.commit()
    session.refresh(cliente_nuevo)
    return cliente_nuevo


@router.delete("/clientes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(id: int, session: SessionDeDependencia, token: Token_Dependencia):

    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta information")

    consulta = select(Cliente).where(Cliente.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.put("/clientes/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
async def update_cliente(id: int, datos_cliente: ClienteUpdate, session: SessionDeDependencia):
    consulta = select(Cliente).where(Cliente.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    resultado.nombre = datos_cliente.nombre
    resultado.apellido = datos_cliente.apellido
    resultado.telefono = datos_cliente.telefono
    resultado.email = datos_cliente.email
    resultado.direccion = datos_cliente.direccion
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
