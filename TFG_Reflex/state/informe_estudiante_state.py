import reflex as rx
import sqlmodel
from datetime import datetime
from typing import List, Dict, Any
from ..state.base_state import BaseState
from ..models.usuarios import Usuario, Docente, Estudiante, Grupos, EstudianteGrupo
from ..models.tarea import Tarea, Ejercicio, PruebaEvaluacion
from ..models.evaluacion import ResolucionTarea, RespuestaPregunta

class InformeEstudianteState(BaseState):
    estudiante_uid: str = ""
    estudiante_nombre: str = ""
    estudiante_correo: str = ""
    
    total_completadas: int = 0
    nota_media: float = 0.0
    
    detalles_tareas: List[Dict[str, Any]] = []
    
    datos_grafico: List[Dict[str, Any]] = []

    def cargar_informe(self):
        self.estudiante_uid = self.router.page.params.get("id_estudiante", "")
        if not self.estudiante_uid:
            return rx.redirect("/mis-grupos")
            
        with rx.session() as session:
            if not self.usuario_actual:
                return rx.redirect("/login")
                
            estudiante_user = session.exec(
                sqlmodel.select(Usuario).where(Usuario.id_usuario == int(self.estudiante_uid))
            ).first()
            
            if not estudiante_user:
                return rx.redirect("/mis-grupos")
                
            self.estudiante_nombre = estudiante_user.nombreUsuario
            self.estudiante_correo = estudiante_user.correo
            
            docente_actual = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            
            if not docente_actual or docente_actual.rol != "docente":
                return rx.redirect("/dashboard")
                
            grupos_docente = session.exec(
                sqlmodel.select(Grupos).where(Grupos.docente_id == docente_actual.id_usuario)
            ).all()
            ids_grupos = [g.id_grupo for g in grupos_docente]
                
            condiciones_tarea = (Tarea.docente_id == docente_actual.id_usuario)
            if ids_grupos:
                condiciones_tarea = condiciones_tarea | (Tarea.grupo_id.in_(ids_grupos))
                
            statement = sqlmodel.select(ResolucionTarea, Tarea).join(Tarea).where(
                (ResolucionTarea.estudiante_id == int(self.estudiante_uid)) &
                condiciones_tarea &
                (sqlmodel.func.lower(ResolucionTarea.estado) == "corregida")
            ).order_by(ResolucionTarea.fechaEntrega)
            
            resultados = session.exec(statement).all()
            
            if not resultados:
                self.total_completadas = 0
                self.nota_media = 0.0
                self.detalles_tareas = []
                self.datos_grafico = []
                return
                
            self.total_completadas = len(resultados)
            suma_notas_base_10 = 0.0
            
            self.detalles_tareas = []
            self.datos_grafico = []
            
            for index, (resolucion, tarea) in enumerate(resultados):
                
                es_ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first() is not None
                tipo_str = "Ejercicio" if es_ejercicio else "Prueba de Evaluación"
                
                respuestas = session.exec(
                    sqlmodel.select(RespuestaPregunta).where(RespuestaPregunta.resolucion_id == resolucion.id)
                ).all()
                
                comentarios = []
                for resp in respuestas:
                    if resp.retroalimentacion and resp.retroalimentacion.strip():
                        comentarios.append(resp.retroalimentacion)
                        
                comentario_general = " | ".join(comentarios) if comentarios else "Sin comentarios específicos."
                
                fecha_str = resolucion.fechaEntrega.strftime("%d/%m/%Y")
                
                from ..models.tarea import Pregunta
                preguntas_tarea = session.exec(sqlmodel.select(Pregunta).where(Pregunta.tarea_id == tarea.id_tarea)).all()
                suma_maximas = sum(float(p.calificacion_maxima) for p in preguntas_tarea) if preguntas_tarea else 10.0
                if suma_maximas == 0:
                    suma_maximas = 10.0
                    
                calif_obtenida = float(resolucion.calificacionTotal)
                calif_base_10 = (calif_obtenida / suma_maximas) * 10.0
                suma_notas_base_10 += calif_base_10
                
                aprobado = calif_obtenida >= (suma_maximas / 2.0)
                
                self.detalles_tareas.append({
                    "tarea_id": str(tarea.id_tarea),
                    "titulo": tarea.titulo,
                    "tipo": tipo_str,
                    "fecha": fecha_str,
                    "calificacion": calif_obtenida,
                    "aprobado": aprobado,
                    "comentarios": comentario_general
                })
                
                titulo_corto = tarea.titulo[:15] + "..." if len(tarea.titulo) > 15 else tarea.titulo
                self.datos_grafico.append({
                    "nombre": titulo_corto,
                    "calificacion": round(calif_base_10, 2)
                })
                
            self.nota_media = round(suma_notas_base_10 / self.total_completadas, 2)
