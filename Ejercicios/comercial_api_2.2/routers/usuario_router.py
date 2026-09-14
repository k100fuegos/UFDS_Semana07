from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from config.session_Dependencia import SessionDeDependencia
from models.rol import Rol
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioUpdatePatch
from lib.pwd import get_password_hash

router = APIRouter()


def validar_username_disponible(session, username: str, id_usuario: int | None = None):
    consulta = select(Usuario).where(Usuario.username == username)
    if id_usuario is not None:
        consulta = consulta.where(Usuario.id != id_usuario)
    if session.exec(consulta).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El username ya está registrado"
        )


@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
async def get_usuarios(session: SessionDeDependencia,
                       offset: int = Query(0, ge=0),
                       limit: int = Query(20, ge=1)):
    consulta = select(Usuario).offset(offset).limit(limit)
    resultado = session.exec(consulta)
    return resultado.all()


@router.get("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resultado


@router.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def create_usuario(datos_usuario: UsuarioCreate, session: SessionDeDependencia):
    validar_username_disponible(session, datos_usuario.username)

    rol = session.exec(select(Rol).where(
        Rol.id == datos_usuario.id_rol)).first()
    if not rol:
        raise HTTPException(
            status_code=404, detail=f"Rol con id {datos_usuario.id_rol} no encontrado")

    usuario_nuevo = Usuario(
        username=datos_usuario.username,
        password=get_password_hash(datos_usuario.password),
        nombre=datos_usuario.nombre,
        apellido=datos_usuario.apellido,
        telefono=datos_usuario.telefono,
        correo=datos_usuario.correo,
        id_rol=datos_usuario.id_rol,
    )
    session.add(usuario_nuevo)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El username ya está registrado"
        )
    session.refresh(usuario_nuevo)
    return usuario_nuevo


@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(resultado)
    session.commit()
    return None


@router.put("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def update_usuario(id: int, datos_usuario: UsuarioUpdate, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado = session.exec(consulta).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    rol = session.exec(select(Rol).where(
        Rol.id == datos_usuario.id_rol)).first()
    if not rol:
        raise HTTPException(
            status_code=404, detail=f"Rol con id {datos_usuario.id_rol} no encontrado")

    validar_username_disponible(session, datos_usuario.username, id)
    resultado.username = datos_usuario.username
    resultado.password = get_password_hash(datos_usuario.password)
    resultado.nombre = datos_usuario.nombre
    resultado.apellido = datos_usuario.apellido
    resultado.telefono = datos_usuario.telefono

    if datos_usuario.correo:
        resultado.correo = datos_usuario.correo

    resultado.id_rol = datos_usuario.id_rol
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado


@router.patch('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos_usuario: UsuarioUpdatePatch, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado = session.exec(consulta).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos_usuario.id_rol:
        rol = session.exec(select(Rol).where(
            Rol.id == datos_usuario.id_rol)).first()
        if not rol:
            raise HTTPException(
                status_code=404, detail=f"Rol con id {datos_usuario.id_rol} no encontrado")

    if (datos_usuario.username is not None
            and datos_usuario.username != resultado.username):
        validar_username_disponible(session, datos_usuario.username, id)

    datos_actualizados = datos_usuario.model_dump(exclude_unset=True)
    if "password" in datos_actualizados:
        datos_actualizados["password"] = get_password_hash(
            datos_actualizados["password"]
        )

    resultado.sqlmodel_update(datos_actualizados)
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
