from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from config.session_Dependencia import SessionDeDependencia
from models.rol import Rol
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from lib.pwd import get_password_hash

router = APIRouter()


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
    session.commit()
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


@router.patch("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos_usuario: UsuarioUpdatePatch, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    usuario = session.exec(consulta).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos_usuario.id_rol is not None:
        rol = session.exec(select(Rol).where(
            Rol.id == datos_usuario.id_rol)).first()
        if not rol:
            raise HTTPException(
                status_code=404, detail=f"Rol con id {datos_usuario.id_rol} no encontrado")
        usuario.id_rol = datos_usuario.id_rol

    if datos_usuario.username is not None:
        usuario.username = datos_usuario.username
    if datos_usuario.password is not None:
        usuario.password = get_password_hash(datos_usuario.password)
    if datos_usuario.nombre is not None:
        usuario.nombre = datos_usuario.nombre
    if datos_usuario.apellido is not None:
        usuario.apellido = datos_usuario.apellido
    if datos_usuario.telefono is not None:
        usuario.telefono = datos_usuario.telefono
    if datos_usuario.correo is not None:
        usuario.correo = datos_usuario.correo
    if datos_usuario.correo is None and hasattr(datos_usuario, "correo"):
        usuario.correo = None

    usuario.updated_at = datetime.utcnow()

    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


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

    resultado.username = datos_usuario.username
    resultado.password = get_password_hash(datos_usuario.password)
    resultado.nombre = datos_usuario.nombre
    resultado.apellido = datos_usuario.apellido
    resultado.telefono = datos_usuario.telefono
    resultado.correo = datos_usuario.correo
    resultado.id_rol = datos_usuario.id_rol
    resultado.updated_at = datetime.utcnow()

    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado


@router.patch('/usuarios/{id}', response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos_usuario: UsuarioUpdate, session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado = session.exec(consulta).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if datos_usuario.correo:
        resultado.correo = datos_usuario.correo

    resultado.password = get_password_hash(password)
    session.add(resultado)
    session.commit()
    session.refresh(resultado)
    return resultado
