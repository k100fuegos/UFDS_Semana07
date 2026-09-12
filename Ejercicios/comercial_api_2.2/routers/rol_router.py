from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.rol import Rol, RolCreate, RolUpdate

router = APIRouter()


@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
async def get_roles(session: SessionDeDependencia,
                    offset: int = Query(0, ge=0),
                    limit: int = Query(20, ge=1)):
    consulta = select(Rol).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
async def get_rol(id: int, session: SessionDeDependencia):
    consulta = select(Rol).where(Rol.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return resultado


@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
async def create_rol(datos_rol: RolCreate, session: SessionDeDependencia):
    rol_nuevo = Rol(nombre=datos_rol.nombre, descripcion=datos_rol.descripcion)
    session.add(rol_nuevo)
    session.commit()
    session.refresh(rol_nuevo)
    return rol_nuevo


@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(id: int, session: SessionDeDependencia):
    consulta = select(Rol).where(Rol.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.put("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
async def update_rol(id: int, datos_rol: RolUpdate, session: SessionDeDependencia):
    consulta = select(Rol).where(Rol.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    resultado.nombre = datos_rol.nombre
    if datos_rol.descripcion is not None:
        resultado.descripcion = datos_rol.descripcion
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
