from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.tipo_pago import TipoPago, TipoPagoCreate, TipoPagoUpdate
from config.security_Dependencia import Token_Dependencia

router = APIRouter()


@router.get("/tipos-pago", response_model=list[TipoPago], status_code=status.HTTP_200_OK)
async def get_tipos_pago(session: SessionDeDependencia,
                         offset: int = Query(0, ge=0),
                         limit: int = Query(20, ge=1)):
    consulta = select(TipoPago).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/tipos-pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
async def get_tipo_pago(id: int, session: SessionDeDependencia):
    consulta = select(TipoPago).where(TipoPago.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=404, detail="Tipo de pago no encontrado")
    return resultado


@router.post("/tipos-pago", response_model=TipoPago, status_code=status.HTTP_201_CREATED)
async def create_tipo_pago(datos_tipo_pago: TipoPagoCreate, session: SessionDeDependencia, token: Token_Dependencia = Token_Dependencia()):

    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta information")

    tipo_pago_nuevo = TipoPago(
        nombre=datos_tipo_pago.nombre,
        descripcion=datos_tipo_pago.descripcion,
    )
    session.add(tipo_pago_nuevo)
    session.commit()
    session.refresh(tipo_pago_nuevo)
    return tipo_pago_nuevo


@router.delete("/tipos-pago/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tipo_pago(id: int, session: SessionDeDependencia, token: Token_Dependencia):

    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta information")

    consulta = select(TipoPago).where(TipoPago.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=404, detail="Tipo de pago no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.put("/tipos-pago/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
async def update_tipo_pago(id: int, datos_tipo_pago: TipoPagoUpdate, session: SessionDeDependencia, token: Token_Dependencia = Token_Dependencia()):

    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta information")

    consulta = select(TipoPago).where(TipoPago.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=404, detail="Tipo de pago no encontrado")

    resultado.nombre = datos_tipo_pago.nombre
    if datos_tipo_pago.descripcion is not None:
        resultado.descripcion = datos_tipo_pago.descripcion
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
