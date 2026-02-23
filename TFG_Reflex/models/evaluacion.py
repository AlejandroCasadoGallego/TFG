import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .usuarios import Estudiante
    from .tarea import Pregunta, Tarea

# =======================================================
# PAQUETE: G. DE EVALUACIÓN
# =======================================================

class ResolucionTarea(rx.Model, table=True):
    fechaEntrega: datetime
    calificacionTotal: float = sqlmodel.Field(default=0.0)
    estado: str 
    
    estudiante_id: int = sqlmodel.Field(foreign_key="estudiante.usuario_id")
    tarea_id: int = sqlmodel.Field(foreign_key="tarea.id_tarea")
    
    estudiante: Optional["Estudiante"] = sqlmodel.Relationship(back_populates="resoluciones")
    tarea: Optional["Tarea"] = sqlmodel.Relationship(back_populates="resoluciones")
    
    respuestas: List["RespuestaPregunta"] = sqlmodel.Relationship(back_populates="resolucion")

class RespuestaPregunta(rx.Model, table=True):
    respuesta: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    calificacion: float = sqlmodel.Field(default=0.0)
    retroalimentacion: Optional[str] = sqlmodel.Field(default=None, sa_type=sqlmodel.Text)
    
    resolucion_id: int = sqlmodel.Field(foreign_key="resoluciontarea.id")
    pregunta_id: int = sqlmodel.Field(foreign_key="pregunta.id")
    
    resolucion: Optional["ResolucionTarea"] = sqlmodel.Relationship(back_populates="respuestas")
    pregunta: Optional["Pregunta"] = sqlmodel.Relationship(back_populates="respuestas_alumnos")