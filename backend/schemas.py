from pydantic import BaseModel, ConfigDict
from typing import Optional, List

# ======== Esquemas de Alumnos ========

class AlumnoBase(BaseModel):
    id_grupo: int
    nombre: str
    apellidos: str
    email: Optional[str] = None

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoResponse(AlumnoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# ======== Esquemas de Grupos ========

class GrupoBase(BaseModel):
    id_profesor: str
    nombre: str
    ciclo: str
    curso: str
    color: Optional[str] = 'bg-blue-600'

class GrupoUpdateColor(BaseModel):
    color: str

class GrupoCreate(GrupoBase):
    pass

class GrupoResponse(GrupoBase):
    id: int
    alumnos: List[AlumnoResponse] = []
    
    model_config = ConfigDict(from_attributes=True)