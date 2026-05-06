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

    alumnos_docente: list[dict] = []

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
            
        from ..models.usuarios import Grupos, EstudianteGrupo
        from sqlalchemy.orm import aliased
        
        grupos_doc = session.exec(sqlmodel.select(Grupos).where(Grupos.docente_id == usuario.id_usuario)).all()
        ids_grupos = [g.id_grupo for g in grupos_doc]
        
        self.alumnos_docente = []
        if ids_grupos:
            estudiantes = session.exec(
                sqlmodel.select(Usuario, Grupos.nombre)
                .join(EstudianteGrupo, Usuario.id_usuario == EstudianteGrupo.estudiante_id)
                .join(Grupos, EstudianteGrupo.grupo_id == Grupos.id_grupo)
                .where(Grupos.id_grupo.in_(ids_grupos))
                .distinct()
            ).all()
            
            for est, nom_grupo in estudiantes:
                self.alumnos_docente.append({
                    "id": str(est.id_usuario),
                    "nombre": est.nombreUsuario,
                    "grupo": nom_grupo,
                    "iniciales": est.nombreUsuario[:2].upper()
                })

    def _cargar_stats_estudiante(self, session, usuario):
        from ..models.tarea import EstudianteTarea, Ejercicio, Pregunta

        ahora = datetime.now()

        resultados = session.exec(
            sqlmodel.select(Tarea, EstudianteTarea)
            .join(EstudianteTarea, Tarea.id_tarea == EstudianteTarea.id_tarea)
            .where(EstudianteTarea.id_estudiante == usuario.id_usuario)
        ).all()

        count_pendientes = 0
        count_completadas = 0
        suma_base_10 = 0.0

        for tarea, estudiante_tarea in resultados:
            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea).where(
                    (ResolucionTarea.tarea_id == tarea.id_tarea) &
                    (ResolucionTarea.estudiante_id == usuario.id_usuario)
                )
            ).first()

            if resolucion and resolucion.estado == "corregida" and resolucion.calificacion_liberada:
                count_completadas += 1
                preguntas_tarea = session.exec(sqlmodel.select(Pregunta).where(Pregunta.tarea_id == tarea.id_tarea)).all()
                suma_maximas = sum(float(p.calificacion_maxima) for p in preguntas_tarea) if preguntas_tarea else 10.0
                if suma_maximas == 0:
                    suma_maximas = 10.0
                suma_base_10 += (float(resolucion.calificacionTotal) / suma_maximas) * 10.0
            elif tarea.fechaFin >= ahora:
                ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first()
                permite_reintentos = ejercicio.permiteReintentos if ejercicio else False
                if resolucion and not permite_reintentos:
                    pass
                else:
                    count_pendientes += 1

        self.tareas_pendientes = str(count_pendientes)
        self.tareas_completadas = str(count_completadas)
        self.mi_media = f"{(suma_base_10 / count_completadas):.1f}" if count_completadas > 0 else "0.0"

