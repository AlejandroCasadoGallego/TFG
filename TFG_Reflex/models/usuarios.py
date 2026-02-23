import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .tarea import Tarea
    from .evaluacion import ResolucionTarea
# =======================================================
# PAQUETE: G. DE USUARIOS
# =======================================================

class Usuario(rx.Model, table=True):
    """Clase base para todos los usuarios."""
    id_usuario: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    
    nombreUsuario: str = sqlmodel.Field(max_length=100)
    contraseñaHash: str = sqlmodel.Field(max_length=255)
    correo: str = sqlmodel.Field(unique=True, max_length=150)
    fechaRegistro: datetime = sqlmodel.Field(default_factory=datetime.now)
    rol: str = sqlmodel.Field(default="estudiante") # Valores: 'admin', 'docente', 'estudiante'

class EstudianteGrupo(rx.Model, table=True):
    """Tabla intermedia N:M"""
    estudiante_id: int = sqlmodel.Field(foreign_key="estudiante.usuario_id", primary_key=True)
    grupo_id: int = sqlmodel.Field(foreign_key="grupos.id_grupo", primary_key=True)

class Administrador(rx.Model, table=True):
    usuario_id: int = sqlmodel.Field(foreign_key="usuario.id_usuario", primary_key=True)

class Docente(rx.Model, table=True):
    usuario_id: int = sqlmodel.Field(foreign_key="usuario.id_usuario", primary_key=True)

    grupos: List["Grupos"] = sqlmodel.Relationship(back_populates="docente")
    tareas: List["Tarea"] = sqlmodel.Relationship(back_populates="docente")

class Estudiante(rx.Model, table=True):
    usuario_id: int = sqlmodel.Field(foreign_key="usuario.id_usuario", primary_key=True)
    
    resoluciones: List["ResolucionTarea"] = sqlmodel.Relationship(back_populates="estudiante")
    
    grupos: List["Grupos"] = sqlmodel.Relationship(
        back_populates="estudiantes", 
        link_model=EstudianteGrupo
    )

class Grupos(rx.Model, table=True):
    id_grupo: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    nombre: str = sqlmodel.Field(max_length=100)
    
    docente_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="docente.usuario_id")
    docente: Optional["Docente"] = sqlmodel.Relationship(back_populates="grupos")

    estudiantes: List["Estudiante"] = sqlmodel.Relationship(
        back_populates="grupos",
        link_model=EstudianteGrupo
    )
    
    tareas: List["Tarea"] = sqlmodel.Relationship(back_populates="grupo")