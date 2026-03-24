import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
import random
import string
from datetime import datetime

if TYPE_CHECKING:
    from .tarea import Tarea
    from .evaluacion import ResolucionTarea

class Usuario(sqlmodel.SQLModel, table=True):
    id_usuario: int | None = sqlmodel.Field(default=None, primary_key=True)
    nombreUsuario: str
    correo: str = sqlmodel.Field(unique=True)
    contraseñaHash: str
    rol: str
    activo: bool = sqlmodel.Field(default=True)
    debe_cambiar_pass: bool = sqlmodel.Field(default=False)

class EstudianteGrupo(rx.Model, table=True):
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
    
    codigo_acceso: str = sqlmodel.Field(unique=True, index=True, max_length=10)

    docente_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="docente.usuario_id")
    docente: Optional["Docente"] = sqlmodel.Relationship(back_populates="grupos")

    estudiantes: List["Estudiante"] = sqlmodel.Relationship(
        back_populates="grupos",
        link_model=EstudianteGrupo
    )
    
    tareas: List["Tarea"] = sqlmodel.Relationship(back_populates="grupo")
    @staticmethod
    def generar_codigo() -> str:
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(random.choice(caracteres) for _ in range(6))
    
class Notificacion(rx.Model, table=True):
    id_notificacion: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    remitente_id: int = sqlmodel.Field(foreign_key="usuario.id_usuario")
    destinatario_id: int = sqlmodel.Field(foreign_key="usuario.id_usuario")
    titulo: str = sqlmodel.Field(max_length=150)
    mensaje: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    leida: bool = sqlmodel.Field(default=False)
    fecha: datetime = sqlmodel.Field(default_factory=datetime.utcnow)