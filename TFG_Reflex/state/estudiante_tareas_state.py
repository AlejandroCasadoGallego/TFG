import reflex as rx
import sqlmodel
from typing import List
from datetime import datetime
from .base_state import BaseState

class EstudianteTareaUI(rx.Base):
    id_tarea: str
    titulo: str
    descripcion: str
    estado: str
    fechas: str
    tipo: str

class EstudianteTareasState(BaseState):
    tareas: List[EstudianteTareaUI] = []

    def cargar_tareas(self):
        if not self.usuario_actual:
            return

        with rx.session() as session:
            from ..models.usuarios import Usuario
            from ..models.tarea import Tarea, EstudianteTarea, Ejercicio, PruebaEvaluacion
            from ..models.evaluacion import ResolucionTarea

            estudiante = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not estudiante:
                return

            ahora = datetime.now()

            statement = (
                sqlmodel.select(Tarea, EstudianteTarea)
                .join(EstudianteTarea, Tarea.id_tarea == EstudianteTarea.id_tarea)
                .where(
                    (EstudianteTarea.id_estudiante == estudiante.id_usuario) &
                    (Tarea.fechaFin >= ahora)
                )
                .order_by(Tarea.fechaFin.asc())
            )
            
            resultados = session.exec(statement).all()

            lista_tareas = []
            for tarea, estudiante_tarea in resultados:
                ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first()
                prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == tarea.id_tarea)).first()
                
                
                resolucion = session.exec(
                    sqlmodel.select(ResolucionTarea).where(
                        (ResolucionTarea.tarea_id == tarea.id_tarea) &
                        (ResolucionTarea.estudiante_id == estudiante.id_usuario)
                    )
                ).first()

                permite_reintentos = False
                if ejercicio:
                    permite_reintentos = ejercicio.permiteReintentos
                
                
                if resolucion and not permite_reintentos:
                    continue

                tipo = "Ejercicio" if ejercicio else "Prueba" if prueba else "Tarea"

                lista_tareas.append(EstudianteTareaUI(
                    id_tarea=str(tarea.id_tarea),
                    titulo=tarea.titulo,
                    descripcion=tarea.descripcion if tarea.descripcion else "Sin descripción",
                    estado=estudiante_tarea.estado.capitalize(),
                    fechas=f"Hasta {tarea.fechaFin.strftime('%d/%m/%Y %H:%M')}",
                    tipo=tipo
                ))
            
            self.tareas = lista_tareas

    def ir_a_tarea(self, id_tarea: str):
        return rx.redirect(f"/resolver-tarea/{id_tarea}")
