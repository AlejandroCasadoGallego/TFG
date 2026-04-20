import reflex as rx
import sqlmodel
from datetime import datetime
from .base_state import BaseState
from ..models.usuarios import Usuario, Docente, Grupos
from ..models.tarea import Tarea
from ..models.evaluacion import ResolucionTarea

class DashboardState(BaseState):
    tareas_para_corregir: str = "0"
    tareas_activas: str = "0"
    
    tareas_pendientes: str = "0"
    tareas_completadas: str = "0"
    mi_media: str = "0.0"

    def cargar_estadisticas_dashboard(self):
        if not self.usuario_actual:
            return
            
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not usuario:
                return

            if usuario.rol == "docente":
                self._cargar_stats_docente(session, usuario)
            elif usuario.rol == "estudiante":
                self._cargar_stats_estudiante(session, usuario)

    def _cargar_stats_docente(self, session, usuario):
        ahora = datetime.now()
        activas = session.exec(
            sqlmodel.select(Tarea).where(
                (Tarea.docente_id == usuario.id_usuario) & 
                (Tarea.fechaFin >= ahora)
            )
        ).all()
        self.tareas_activas = str(len(activas))

        tareas_ids = session.exec(
            sqlmodel.select(Tarea.id_tarea).where(Tarea.docente_id == usuario.id_usuario)
        ).all()
        
        if tareas_ids:
            para_corregir = session.exec(
                sqlmodel.select(ResolucionTarea).where(
                    (ResolucionTarea.tarea_id.in_(tareas_ids)) & 
                    (sqlmodel.func.lower(ResolucionTarea.estado) == "entregado")
                )
            ).all()
            self.tareas_para_corregir = str(len(para_corregir))
        else:
            self.tareas_para_corregir = "0"

    def _cargar_stats_estudiante(self, session, usuario):
        from ..models.usuarios import EstudianteGrupo
        grupos_ids = session.exec(
            sqlmodel.select(EstudianteGrupo.grupo_id).where(EstudianteGrupo.estudiante_id == usuario.id_usuario)
        ).all()
        
        if not grupos_ids:
            self.tareas_pendientes = "0"
            self.tareas_completadas = "0"
            self.mi_media = "0.0"
            return

        ahora = datetime.now()
        tareas_totales = session.exec(
            sqlmodel.select(Tarea).where(
                (Tarea.grupo_id.in_(grupos_ids)) &
                (Tarea.fechaFin >= ahora)
            )
        ).all()
        
        resoluciones = session.exec(
            sqlmodel.select(ResolucionTarea).where(ResolucionTarea.estudiante_id == usuario.id_usuario)
        ).all()
        
        tareas_entregadas_ids = [r.tarea_id for r in resoluciones if r.estado.lower() in ["entregado", "calificado"]]
        
        pendientes = [t for t in tareas_totales if t.id_tarea not in tareas_entregadas_ids]
        self.tareas_pendientes = str(len(pendientes))
        
        completadas = [r for r in resoluciones if r.estado.lower() == "calificado"]
        self.tareas_completadas = str(len(completadas))
        
        if completadas:
            media = sum(r.calificacionTotal for r in completadas) / len(completadas)
            self.mi_media = f"{media:.1f}"
        else:
            self.mi_media = "0.0"
