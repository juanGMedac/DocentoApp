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
    prefix="/api/grupos",
    tags=["grupos"],
)

@router.get("/", response_model=List[schemas.GrupoResponse])
def get_grupos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grupos = db.query(models.Grupo).offset(skip).limit(limit).all()
    return grupos

@router.post("/", response_model=schemas.GrupoResponse, status_code=status.HTTP_201_CREATED)
def create_grupo(grupo: schemas.GrupoCreate, db: Session = Depends(get_db)):
    # Verificar que el profesor exista, utilizando la variable id_profesor corregida
    profesor = db.query(models.Profesor).filter(models.Profesor.id_auth == grupo.id_profesor).first()
    if not profesor:
        # Devolvemos un 404 estricto para validar la integridad de la base de datos
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesor no encontrado")

    # Creamos el grupo mapeando explícitamente TODOS los campos de DocentoApp
    db_grupo = models.Grupo(
        id_profesor=grupo.id_profesor,
        nombre=grupo.nombre,
        ciclo=grupo.ciclo,
        curso=grupo.curso
    )
    
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.get("/{grupo_id}", response_model=schemas.GrupoResponse)
def get_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return grupo

@router.delete("/{grupo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    
    # El borrado en cascada (cascade="all, delete-orphan") de SQLAlchemy se encarga de eliminar a los alumnos.
    db.delete(grupo)
    db.commit()
    return None