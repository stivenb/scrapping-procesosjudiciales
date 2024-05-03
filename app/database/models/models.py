from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    __name__: str

    # to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Causa(Base):
    __tablename__ = 'causa'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    idJuicio = Column(String, unique=True, nullable=False)
    estadoActual = Column(String, nullable=True)
    idMateria = Column(Integer, nullable=True)
    idProvincia = Column(String, nullable=True)
    idCanton = Column(String, nullable=True)
    idJudicatura = Column(String, nullable=True)
    nombreDelito = Column(String, nullable=True)
    fechaIngreso = Column(DateTime, nullable=True)   

     # Relaciones
    incidentes = relationship("Incidente", backref="juicio", cascade="all, delete, delete-orphan")
    
    
class Incidente(Base):
    __tablename__ = 'incidente'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    idIncidenteJudicatura = Column(Integer, nullable=False)
    idMovimientoJuicioIncidente = Column(Integer, nullable=False)
    fechaCrea = Column(DateTime, nullable=True)
    incidente = Column(Integer, nullable=True)
    
    # Foreign Key
    causa_id = Column(Integer, ForeignKey("causa.id"), nullable=False)
    
    # Relaciones
    litigantes = relationship("Litigante", backref="incidente", cascade="all, delete, delete-orphan")
    actuaciones = relationship("Actuacion", backref="incidente", cascade="all, delete, delete-orphan")
     
# Modelo para Litigante
class Litigante(Base):
    __tablename__ = 'litigante'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipoLitigante = Column(String, nullable=True)
    nombresLitigante = Column(String, nullable=True)
    representadoPor = Column(String, nullable=True)
    
    # Foreign Key
    incidente_id = Column(Integer, ForeignKey("incidente.id"), nullable=False)

# Modelo para Actuacion
class Actuacion(Base):
    __tablename__ = 'actuacion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer, nullable=True)
    idJudicatura = Column(String, nullable=True)
    fecha = Column(DateTime, nullable=True)
    tipo = Column(String, nullable=True)
    actividad = Column(Text, nullable=True)
    visible = Column(String, nullable=True)
    origen = Column(String, nullable=True)
    uuid = Column(String, nullable=True)
    nombreArchivo = Column(String, nullable=True)
    
    # Foreign Key
    incidente_id = Column(Integer, ForeignKey("incidente.id"), nullable=False)