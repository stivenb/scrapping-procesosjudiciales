from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ActorOfendido(Base):
    __tablename__ = "actor_ofendido"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ruc = Column(String(50), nullable=False)


class ProcesoOfendido(Base):
    __tablename__ = "proceso_ofendido"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    numero_proceso = Column(String(50), nullable=False)
    accion_infraccion = Column(String(255), nullable=False)
    actor_ofendido_id = Column(Integer, ForeignKey("actor_ofendido.id"))


class MovimientoProceso(Base):
    __tablename__ = "movimiento_proceso"

    numero_proceso = Column(String(50), nullable=False)
    materia = Column(String(255), nullable=False)
    delito_asunto = Column(String(255), nullable=False)
    tipo_ingreso = Column(String(255), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    tipo_accion = Column(String(255), nullable=False)
    nro_proceso_vinculado = Column(String(50), nullable=False)
    proceso_ofendido_id = Column(Integer, ForeignKey("proceso_ofendido.id"))


class ProcesoJudicial(Base):
    __tablename__ = "detalle_movimiento_judicial"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    actores_ofendido = Column(String(255), nullable=False)
    demandados_procesados = Column(String(255), nullable=False)

    numero_proceso = Column(String(50), nullable=False)
    materia = Column(String(255), nullable=False)
    delito = Column(String(255), nullable=False)
    tipo_ingreso = Column(String(255), nullable=False)
    actor_ofendido = Column(String(255), nullable=False)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    tipo_accion = Column(String(255), nullable=False)
    judicatura = Column(String(255), nullable=False)
    nro_proceso_vinculado = Column(String(50), nullable=False)
    demandado_procesado = Column(String(255), nullable=False)

    movimiento_proceso_id = Column(Integer, ForeignKey("movimiento_proceso.id"))


class DetalleProcesoJudicial(Base):
    __tablename__ = "detalle_proceso_judicial"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    detalle = Column(String(255), nullable=False)