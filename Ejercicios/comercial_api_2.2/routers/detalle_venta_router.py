from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.producto import Producto
from models.venta import Venta
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate
from config.security_Dependencia import Token_Dependencia

router = APIRouter()


@router.get("/detalle-ventas", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
async def get_detalles_venta(session: SessionDeDependencia,
                             offset: int = Query(0, ge=0),
                             limit: int = Query(20, ge=1)):
    consulta = select(DetalleVenta).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/detalle-ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def get_detalle_venta(id: int, session: SessionDeDependencia):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=404, detail="Detalle de venta no encontrado")
    return resultado


@router.post("/detalle-ventas", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
async def create_detalle_venta(datos_detalle: DetalleVentaCreate, session: SessionDeDependencia):
    venta = session.exec(select(Venta).where(
        Venta.id == datos_detalle.id_venta)).first()
    if not venta:
        raise HTTPException(
            status_code=404, detail=f"Venta con id {datos_detalle.id_venta} no encontrada")

    producto = session.exec(select(Producto).where(
        Producto.id == datos_detalle.id_producto)).first()
    if not producto:
        raise HTTPException(
            status_code=404, detail=f"Producto con id {datos_detalle.id_producto} no encontrado")

    detalle_nuevo = DetalleVenta(
        id_venta=datos_detalle.id_venta,
        id_producto=datos_detalle.id_producto,
        cantidad=datos_detalle.cantidad,
        precio_unitario=datos_detalle.precio_unitario,
        subtotal=datos_detalle.subtotal,
    )
    session.add(detalle_nuevo)
    session.commit()
    session.refresh(detalle_nuevo)
    return detalle_nuevo


@router.delete("/detalle-ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detalle_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):

    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(
            status_code=404, detail="Detalle de venta no encontrado")

    if token['id_rol'] != 1 and resultado.estado == "FINALIZADA":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para eliminar un detalle de venta finalizada")

    session.delete(resultado)
    session.commit()
    return None


@router.put("/detalle-ventas/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def update_detalle_venta(id: int, datos_detalle: DetalleVentaUpdate, session: SessionDeDependencia, token: Token_Dependencia = Token_Dependencia()):
    consulta = select(DetalleVenta).where(DetalleVenta.id == id)
    resultado = session.exec(consulta).first()

    if token['id_rol'] != 1 and resultado.estado == "FINALIZADA":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="No tienes permisos para actualizar un detalle de venta finalizada")

    if not resultado:
        raise HTTPException(
            status_code=404, detail="Detalle de venta no encontrado")

    venta = session.exec(select(Venta).where(
        Venta.id == datos_detalle.id_venta)).first()
    if not venta:
        raise HTTPException(
            status_code=404, detail=f"Venta con id {datos_detalle.id_venta} no encontrada")

    producto = session.exec(select(Producto).where(
        Producto.id == datos_detalle.id_producto)).first()
    if not producto:
        raise HTTPException(
            status_code=404, detail=f"Producto con id {datos_detalle.id_producto} no encontrado")

    resultado.id_venta = datos_detalle.id_venta
    resultado.id_producto = datos_detalle.id_producto
    resultado.cantidad = datos_detalle.cantidad
    resultado.precio_unitario = datos_detalle.precio_unitario
    resultado.subtotal = datos_detalle.subtotal
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
