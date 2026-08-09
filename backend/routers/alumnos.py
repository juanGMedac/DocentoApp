from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import sys

# Agregar el directorio principal al path para importaciones limpias
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/api/alumnos",
    tags=["alumnos"],
)

@router.post("/", response_model=schemas.AlumnoResponse, status_code=status.HTTP_201_CREATED)
def create_alumno(alumno: schemas.AlumnoCreate, db: Session = Depends(get_db)):
    # Verificamos que el grupo al que queremos asignar el alumno realmente exista en Oracle
    grupo = db.query(models.Grupo).filter(models.Grupo.id == alumno.id_grupo).first()
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")

    db_alumno = models.Alumno(**alumno.model_dump())
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)
    return db_alumno

@router.get("/", response_model=List[schemas.AlumnoResponse])
def get_alumnos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Alumno).offset(skip).limit(limit).all()