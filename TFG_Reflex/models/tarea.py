import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .usuarios import Docente, Grupos
    from .patrones import PatronDiseño
    from .evaluacion import ResolucionTarea, RespuestaPregunta

# =======================================================
# PAQUETE: G. ACADEMICA (Tareas y Ejercicios)
# =======================================================

class Tarea(rx.Model, table=True):
    id_tarea: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    titulo: str = sqlmodel.Field(max_length=200)
    descripcion: Optional[str] = sqlmodel.Field(default=None, sa_type=sqlmodel.Text)
    enunciado: Optional[str] = sqlmodel.Field(default=None, sa_type=sqlmodel.Text)
    fechaInicio: datetime
    fechaFin: datetime
    
    docente_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="docente.usuario_id")
    docente: Optional["Docente"] = sqlmodel.Relationship(back_populates="tareas")

    grupo_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="grupos.id_grupo")
    grupo: Optional["Grupos"] = sqlmodel.Relationship(back_populates="tareas")
    
    preguntas: List["Pregunta"] = sqlmodel.Relationship(back_populates="tarea")
    resoluciones: List["ResolucionTarea"] = sqlmodel.Relationship(back_populates="tarea")

class Ejercicio(rx.Model, table=True):
    tarea_id: int = sqlmodel.Field(foreign_key="tarea.id_tarea", primary_key=True)
    
    nivelDificultad: str
    tipoEntrada: str 
    permiteReintentos: bool
    
    patron_id: Optional[int] = sqlmodel.Field(default=None, foreign_key="patrondiseño.id_patron")
    patron: Optional["PatronDiseño"] = sqlmodel.Relationship(back_populates="ejercicios")

class PruebaEvaluacion(rx.Model, table=True):
    tarea_id: int = sqlmodel.Field(foreign_key="tarea.id_tarea", primary_key=True)
    
    fechaInicioPrueba: datetime 
    fechaCierre: datetime
    tiempoLimite: int 

class Pregunta(rx.Model, table=True):
    enunciado: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    tipo: str 
    
    opciones: List[str] = sqlmodel.Field(default=[], sa_type=sqlmodel.JSON)
    respuestaCorrecta: bool 
    
    tarea_id: int = sqlmodel.Field(foreign_key="tarea.id_tarea")
    tarea: Optional["Tarea"] = sqlmodel.Relationship(back_populates="preguntas")
    
    respuestas_alumnos: List["RespuestaPregunta"] = sqlmodel.Relationship(back_populates="pregunta")

class EstudianteTarea(rx.Model, table=True):
    id_estudiante: int = sqlmodel.Field(foreign_key="estudiante.usuario_id", primary_key=True)
    id_tarea: int = sqlmodel.Field(foreign_key="tarea.id_tarea", primary_key=True)
    estado: str = sqlmodel.Field(default="pendiente")