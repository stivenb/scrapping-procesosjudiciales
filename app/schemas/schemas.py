from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator, constr


class Actor(BaseModel):
    cedulaActor: Optional[str] = ""
    nombreActor: Optional[str] = ""



class Demandado(BaseModel):
    cedulaDemandado: Optional[str] = ""
    nombreDemandado: Optional[str] = ""


class CausaJudicial(BaseModel):
    actor: Actor
    demandado: Demandado
    numeroCausa: Optional[str] = ""
    materia: Optional[str] = ""
    numeroFiscalia: Optional[str] = ""
    provincia: Optional[str] = ""
    recaptcha: Optional[str] = "verdad"

class LitiganteDetail(BaseModel):
    tipoLitigante: Optional[str]
    nombresLitigante: Optional[str]
    representadoPor: Optional[str]

class ActuacionDetail(BaseModel):
    codigo: Optional[int]
    idJudicatura: Optional[str]
    fecha: Optional[datetime]
    tipo: Optional[str]
    actividad: Optional[str]
    visible: Optional[str]
    origen: Optional[str]
    uuid: Optional[str]
    nombreArchivo: Optional[str]

class IncidenteDetail(BaseModel):
    idIncidenteJudicatura: Optional[int]
    idMovimientoJuicioIncidente: Optional[int]
    fechaCrea: Optional[datetime]
    incidente: Optional[int]
    litigantes: List[LitiganteDetail] = []
    actuaciones: List[ActuacionDetail] = []

class Causadetail(BaseModel):
    id: int
    idJuicio: str
    estadoActual: Optional[str]
    idMateria: Optional[int]
    idProvincia: Optional[str]
    idCanton: Optional[str]
    idJudicatura: Optional[str]
    nombreDelito: Optional[str]
    fechaIngreso: Optional[datetime]
    incidentes: List[IncidenteDetail] = []
    
    
class UserSignin(BaseModel):
    """
    Clase que representa los datos para el inicio de sesión del usuario.
    """ 
    signin_username: str
    signin_value: constr(min_length=5, max_length=100) 