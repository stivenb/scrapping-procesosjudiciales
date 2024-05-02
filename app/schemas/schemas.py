from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Actor(BaseModel):
    cedulaActor: str
    nombreActor: Optional[str] = ""

    @validator("cedulaActor")
    def validate_cedulaActor_length(cls, v):
        if len(v) < 3:
            raise ValueError("La cédula del actor debe tener al menos 3 caracteres")
        return v


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