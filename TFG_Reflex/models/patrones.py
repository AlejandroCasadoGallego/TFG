import reflex as rx
import sqlmodel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .tarea import Ejercicio

# =======================================================
# PAQUETE: G. DE PATRONES
# =======================================================

class PatronDiseño(rx.Model, table=True):
    id_patron: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    nombre: str = sqlmodel.Field(max_length=150)
    categoria: str = sqlmodel.Field(max_length=100)
    descripcion: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    diagrama: Optional[str] = sqlmodel.Field(default=None, sa_type=sqlmodel.Text)
    ventajas: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    desventajas: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    pseudocodigo: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    ejemplos: str = sqlmodel.Field(sa_type=sqlmodel.Text)
    
    ejercicios: List["Ejercicio"] = sqlmodel.Relationship(back_populates="patron")