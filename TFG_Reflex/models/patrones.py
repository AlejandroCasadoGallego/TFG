import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime

if TYPE_CHECKING:
    from .tarea import Ejercicio

class PatronDiseño(rx.Model, table=True):
    id_patron: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    nombre: str = sqlmodel.Field(max_length=150)
    categoria: str = sqlmodel.Field(max_length=100)
    descripcion: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    diagrama: Optional[str] = sqlmodel.Field(default=None, sa_type=LONGTEXT)
    ventajas: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    desventajas: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    pseudocodigo: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    ejemplos: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    activo: bool = sqlmodel.Field(default=True)
    
    ejercicios: List["Ejercicio"] = sqlmodel.Relationship(back_populates="patron")

class PatronRelacion(rx.Model, table=True):
    patron_origen_id: int = sqlmodel.Field(foreign_key="patrondiseño.id_patron")
    patron_destino_id: int = sqlmodel.Field(foreign_key="patrondiseño.id_patron")
    nombre_relacion: str = sqlmodel.Field(max_length=200)
    descripcion: str = sqlmodel.Field(max_length=300, default="")