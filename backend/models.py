from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Profesor(Base):
    __tablename__ = "profesores"

    id_auth = Column(String(128), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # Relación bidireccional con Grupo, con borrado en cascada
    grupos = relationship("Grupo", back_populates="profesor", cascade="all, delete-orphan")

class Grupo(Base):
    __tablename__ = 'grupos'
    
    id = Column(Integer, primary_key=True, index=True)
    id_profesor = Column(String, ForeignKey('profesores.id_auth'), nullable=False)
    nombre = Column(String, nullable=False)
    ciclo = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    
    # Relaciones
    profesor = relationship("Profesor", back_populates="grupos")
    alumnos = relationship("Alumno", back_populates="grupo", cascade="all, delete-orphan")

class Alumno(Base):
    __tablename__ = 'alumnos'
    
    id = Column(Integer, primary_key=True, index=True)
    id_grupo = Column("ID_GRUPO", Integer, ForeignKey('grupos.id'), nullable=False)
    nombre = Column("NOMBRE", String, nullable=False)
    apellidos = Column("APELLIDOS", String, nullable=False)
    email = Column("EMAIL", String)
    
    # Relación inversa con Grupo
    grupo = relationship("Grupo", back_populates="alumnos")
