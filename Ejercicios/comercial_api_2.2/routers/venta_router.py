from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.cliente import Cliente
from models.usuario import Usuario
from models.tipo_pago import TipoPago
from models.venta import Venta, VentaCreate, VentaUpdate
from config.security_Dependencia import Token_Dependencia

router = APIRouter()


@router.get("/ventas", response_model=list[Venta], status_code=status.HTTP_200_OK)
async def get_ventas(session: SessionDeDependencia,
                     offset: int = Query(0, ge=0),
                     limit: int = Query(20, ge=1)):
    consulta = select(Venta).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
async def get_venta(id: int, session: SessionDeDependencia):
    consulta = select(Venta).where(Venta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return resultado


@router.post("/ventas", response_model=Venta, status_code=status.HTTP_201_CREATED)
async def create_venta(datos_venta: VentaCreate, session: SessionDeDependencia):
    cliente = session.exec(select(Cliente).where(
        Cliente.id == datos_venta.id_cliente)).first()
    if not cliente:
        raise HTTPException(
            status_code=404, detail=f"Cliente con id {datos_venta.id_cliente} no encontrado")

    usuario = session.exec(select(Usuario).where(
        Usuario.id == datos_venta.id_usuario)).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {datos_venta.id_usuario} no encontrado")

    tipo_pago = session.exec(select(TipoPago).where(
        TipoPago.id == datos_venta.id_tipo_pago)).first()
    if not tipo_pago:
        raise HTTPException(
            status_code=404, detail=f"Tipo de pago con id {datos_venta.id_tipo_pago} no encontrado")

    venta_nueva = Venta(
        fecha=datos_venta.fecha,
        id_cliente=datos_venta.id_cliente,
        id_usuario=datos_venta.id_usuario,
        id_tipo_pago=datos_venta.id_tipo_pago,
        subtotal=datos_venta.subtotal,
        iva=datos_venta.iva,
        total=datos_venta.total,
        estado=datos_venta.estado,
    )
    session.add(venta_nueva)
    session.commit()
    session.refresh(venta_nueva)
    return venta_nueva


@router.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):

    if token['id_rol'] != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para acceder a esta information")

    consulta = select(Venta).where(Venta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    resultado.estado = "ANULADA"
    resultado.updated_at = datetime.utcnow()
    session.add(resultado)
    session.commit()
    return None


@router.put("/ventas/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
async def update_venta(id: int, datos_venta: VentaUpdate, session: SessionDeDependencia):
    consulta = select(Venta).where(Venta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    cliente = session.exec(select(Cliente).where(
        Cliente.id == datos_venta.id_cliente)).first()
    if not cliente:
        raise HTTPException(
            status_code=404, detail=f"Cliente con id {datos_venta.id_cliente} no encontrado")

    usuario = session.exec(select(Usuario).where(
        Usuario.id == datos_venta.id_usuario)).first()
    if not usuario:
        raise HTTPException(
            status_code=404, detail=f"Usuario con id {datos_venta.id_usuario} no encontrado")

    tipo_pago = session.exec(select(TipoPago).where(
        TipoPago.id == datos_venta.id_tipo_pago)).first()
    if not tipo_pago:
        raise HTTPException(
            status_code=404, detail=f"Tipo de pago con id {datos_venta.id_tipo_pago} no encontrado")

    resultado.fecha = datos_venta.fecha
    resultado.id_cliente = datos_venta.id_cliente
    resultado.id_usuario = datos_venta.id_usuario
    resultado.id_tipo_pago = datos_venta.id_tipo_pago
    resultado.subtotal = datos_venta.subtotal
    resultado.iva = datos_venta.iva
    resultado.total = datos_venta.total
    resultado.estado = datos_venta.estado
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
