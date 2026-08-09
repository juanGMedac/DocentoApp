from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# ══════════════════════════════════════════════
#  Tabla intermedia: matrículas (Alumno <-> ModuloFP)
# ══════════════════════════════════════════════
matriculas = Table(
    'matriculas',
    Base.metadata,
    Column('id_alumno', Integer, ForeignKey('alumnos.id', ondelete='CASCADE'), primary_key=True),
    Column('id_modulo', Integer, ForeignKey('modulos_fp.id', ondelete='CASCADE'), primary_key=True),
)

class Profesor(Base):
    __tablename__ = "profesores"

    id_auth = Column(String(128), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # Relación bidireccional con Grupo, con borrado en cascada
    grupos = relationship("Grupo", back_populates="profesor", cascade="all, delete-orphan")
    modulos = relationship("ModuloFP", back_populates="profesor", cascade="all, delete-orphan")

class Grupo(Base):
    __tablename__ = 'grupos'

    id = Column(Integer, primary_key=True, index=True)
    id_profesor = Column(String, ForeignKey('profesores.id_auth'), nullable=False)
    nombre = Column(String, nullable=False)
    ciclo = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    color = Column(String, nullable=True, default='bg-blue-600')

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
    # Relación many-to-many con ModuloFP a través de matriculas
    modulos = relationship("ModuloFP", secondary=matriculas, back_populates="alumnos")

class ModuloFP(Base):
    __tablename__ = 'modulos_fp'

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), nullable=False)
    nombre = Column(String(200), nullable=False)
    id_profesor = Column(String(128), ForeignKey('profesores.id_auth'), nullable=False)

    # Relaciones
    profesor = relationship("Profesor", back_populates="modulos")
    # Relación many-to-many con Alumno a través de matriculas
    alumnos = relationship("Alumno", secondary=matriculas, back_populates="modulos")
