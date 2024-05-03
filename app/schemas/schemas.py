from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


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