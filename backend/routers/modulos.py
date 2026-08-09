from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/modulos",
    tags=["modulos"],
)

# ──────────────────────────────────────────────
#  GET /  — Listar todos los módulos
# ──────────────────────────────────────────────
@router.get("/", response_model=List[schemas.ModuloFPResponse])
def get_modulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ModuloFP).offset(skip).limit(limit).all()

# ──────────────────────────────────────────────
#  POST /  — Crear un módulo
# ──────────────────────────────────────────────
@router.post("/", response_model=schemas.ModuloFPResponse, status_code=status.HTTP_201_CREATED)
def create_modulo(modulo: schemas.ModuloFPCreate, db: Session = Depends(get_db)):
    # Verificar que el profesor existe
    profesor = db.query(models.Profesor).filter(models.Profesor.id_auth == modulo.id_profesor).first()
    if not profesor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")

    db_modulo = models.ModuloFP(
        codigo=modulo.codigo,
        nombre=modulo.nombre,
        id_profesor=modulo.id_profesor,
    )
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

# ──────────────────────────────────────────────
#  GET /{id}  — Obtener un módulo por ID
# ──────────────────────────────────────────────
@router.get("/{modulo_id}", response_model=schemas.ModuloFPResponse)
def get_modulo(modulo_id: int, db: Session = Depends(get_db)):
    modulo = db.query(models.ModuloFP).filter(models.ModuloFP.id == modulo_id).first()
    if not modulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado")
    return modulo

# ──────────────────────────────────────────────
#  DELETE /{id}  — Eliminar un módulo
# ──────────────────────────────────────────────
@router.delete("/{modulo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_modulo(modulo_id: int, db: Session = Depends(get_db)):
    modulo = db.query(models.ModuloFP).filter(models.ModuloFP.id == modulo_id).first()
    if not modulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado")
    db.delete(modulo)
    db.commit()
    return None

# ──────────────────────────────────────────────
#  POST /{id}/matricular  — Matriculación masiva
# ──────────────────────────────────────────────
@router.post("/{modulo_id}/matricular", response_model=schemas.ModuloFPResponse)
def matricular_alumnos(modulo_id: int, payload: schemas.MatriculaMasivaRequest, db: Session = Depends(get_db)):
    modulo = db.query(models.ModuloFP).filter(models.ModuloFP.id == modulo_id).first()
    if not modulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado")

    ya_matriculados = {alumno.id for alumno in modulo.alumnos}
    nuevos = 0

    for id_alumno in payload.ids_alumno:
        if id_alumno in ya_matriculados:
            continue  # Evitar duplicados

        alumno = db.query(models.Alumno).filter(models.Alumno.id == id_alumno).first()
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Alumno con id {id_alumno} no encontrado"
            )
        modulo.alumnos.append(alumno)
        nuevos += 1

    db.commit()
    db.refresh(modulo)
    return modulo

# ──────────────────────────────────────────────
#  DELETE /{id}/desmatricular/{id_alumno}  — Desmatriculación individual
# ──────────────────────────────────────────────
@router.delete("/{modulo_id}/desmatricular/{id_alumno}", status_code=status.HTTP_204_NO_CONTENT)
def desmatricular_alumno(modulo_id: int, id_alumno: int, db: Session = Depends(get_db)):
    modulo = db.query(models.ModuloFP).filter(models.ModuloFP.id == modulo_id).first()
    if not modulo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo no encontrado")

    alumno = db.query(models.Alumno).filter(models.Alumno.id == id_alumno).first()
    if not alumno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alumno no encontrado")

    if alumno not in modulo.alumnos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El alumno no está matriculado en este módulo"
        )

    modulo.alumnos.remove(alumno)
    db.commit()
    return None
