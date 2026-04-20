import reflex as rx
import sqlmodel
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import json

from .base_state import BaseState
from ..models.tarea import Tarea, Pregunta, Ejercicio, PruebaEvaluacion, EstudianteTarea
from ..models.evaluacion import ResolucionTarea, RespuestaPregunta
from ..models.usuarios import Usuario

class PreguntaResolucionUI(rx.Base):
    id: int = -1
    enunciado: str = ""
    tipo: str = ""
    opciones: List[str] = []

class TareaResolucionUI(rx.Base):
    id_tarea: int = -1
    titulo: str = ""
    descripcion: str = ""
    enunciado: str = ""

class ResolverTareaState(BaseState):
    tarea_id: int = -1
    tarea_actual: TareaResolucionUI = TareaResolucionUI()
    es_prueba: bool = False
    preguntas: List[PreguntaResolucionUI] = []
    
    respuestas: Dict[int, str] = {}
    
    
    tiempo_restante_segundos: int = 0
    timer_running: bool = False
    
    error_carga: str = ""

    def cargar_tarea(self):
        id_str = self.router.page.params.get("id_tarea", "")
        if not id_str:
            self.error_carga = "ID de tarea no proporcionado."
            return
            
        try:
            self.tarea_id = int(id_str)
        except ValueError:
            self.error_carga = "ID de tarea inválido."
            return

        if not self.usuario_actual:
            return

        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not usuario:
                self.error_carga = "Error de sesión."
                return

            tarea_db = session.exec(sqlmodel.select(Tarea).where(Tarea.id_tarea == self.tarea_id)).first()
            if not tarea_db:
                self.error_carga = "La tarea no existe."
                return
                
            self.tarea_actual = TareaResolucionUI(
                id_tarea=tarea_db.id_tarea or -1,
                titulo=tarea_db.titulo or "",
                descripcion=tarea_db.descripcion or "",
                enunciado=tarea_db.enunciado or ""
            )

            
            asignacion = session.exec(
                sqlmodel.select(EstudianteTarea).where(
                    (EstudianteTarea.id_tarea == self.tarea_id) &
                    (EstudianteTarea.id_estudiante == usuario.id_usuario)
                )
            ).first()
            
            if not asignacion:
                self.error_carga = "No tienes permiso para ver esta tarea."
                return

            
            preguntas_db = session.exec(
                sqlmodel.select(Pregunta).where(Pregunta.tarea_id == self.tarea_id).order_by(Pregunta.id)
            ).all()
            
            self.preguntas = [
                PreguntaResolucionUI(
                    id=p.id,
                    enunciado=p.enunciado or "",
                    tipo=p.tipo or "",
                    opciones=p.opciones or []
                ) for p in preguntas_db
            ]

            
            self.respuestas = {p.id: "" for p in self.preguntas}

            
            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea).where(
                    (ResolucionTarea.tarea_id == self.tarea_id) &
                    (ResolucionTarea.estudiante_id == usuario.id_usuario)
                )
            ).first()

            if resolucion and resolucion.estado == "Entregado":
                ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == self.tarea_id)).first()
                permite_reintentos = False
                if ejercicio:
                    permite_reintentos = ejercicio.permiteReintentos
                    
                if not permite_reintentos:
                    self.error_carga = "Ya has entregado esta tarea. No puedes volver a realizarla."
                    return

            if not resolucion:
                
                resolucion = ResolucionTarea(
                    fechaEntrega=datetime.now(),
                    estado="En progreso",
                    estudiante_id=usuario.id_usuario,
                    tarea_id=self.tarea_id
                )
                session.add(resolucion)
                session.commit()
                session.refresh(resolucion)
                
                
                prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == self.tarea_id)).first()
                if prueba:
                    self.es_prueba = True
                    self.tiempo_restante_segundos = prueba.tiempoLimite * 60
                    self.timer_running = True
                    return ResolverTareaState.tick_timer
                else:
                    self.es_prueba = False
                    self.timer_running = False
            else:
                
                respuestas_bd = session.exec(
                    sqlmodel.select(RespuestaPregunta).where(RespuestaPregunta.resolucion_id == resolucion.id)
                ).all()
                for r in respuestas_bd:
                    if r.respuesta_diagrama and not r.respuesta:
                        self.respuestas[r.pregunta_id] = r.respuesta_diagrama
                    else:
                        self.respuestas[r.pregunta_id] = r.respuesta or ""

                prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == self.tarea_id)).first()
                if prueba:
                    self.es_prueba = True
                    
                    
                    
                    
                    
                    
                    
                    tiempo_transcurrido = (datetime.now() - resolucion.fechaEntrega).total_seconds()
                    restante = (prueba.tiempoLimite * 60) - tiempo_transcurrido
                    if restante <= 0:
                        self.tiempo_restante_segundos = 0
                        self.timer_running = False
                        self.error_carga = "El tiempo de esta prueba ha expirado."
                        return
                    else:
                        self.tiempo_restante_segundos = int(restante)
                        self.timer_running = True
                        return ResolverTareaState.tick_timer
                else:
                    self.es_prueba = False
                    self.timer_running = False

    async def tick_timer(self):
        while self.timer_running:
            await asyncio.sleep(1)
            self.tiempo_restante_segundos -= 1
            if self.tiempo_restante_segundos <= 0:
                yield self.finalizar_tarea(timeout=True)
                break
            yield

    @rx.var
    def tiempo_formateado(self) -> str:
        minutos = self.tiempo_restante_segundos // 60
        segundos = self.tiempo_restante_segundos % 60
        return f"{minutos:02d}:{segundos:02d}"

    def set_respuesta(self, pregunta_id: int, valor: str):
        self.respuestas[pregunta_id] = valor

    def set_diagrama(self, pregunta_id: int, elements: str):
        
        self.respuestas[pregunta_id] = elements

    def finalizar_tarea(self, timeout: bool = False):
        if not self.usuario_actual or self.tarea_id == -1:
            return

        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not usuario:
                return

            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea).where(
                    (ResolucionTarea.tarea_id == self.tarea_id) &
                    (ResolucionTarea.estudiante_id == usuario.id_usuario)
                )
            ).first()

            if not resolucion:
                return

            
            respuestas_viejas = session.exec(
                sqlmodel.select(RespuestaPregunta).where(RespuestaPregunta.resolucion_id == resolucion.id)
            ).all()
            for r in respuestas_viejas:
                session.delete(r)
            session.commit()

            
            for p in self.preguntas:
                valor = self.respuestas.get(p.id, "")
                
                nueva_res = RespuestaPregunta(
                    resolucion_id=resolucion.id,
                    pregunta_id=p.id,
                    calificacion=0.0
                )
                
                if p.tipo.lower() not in ["desarrollo", "test", "desarrollo ", "test "]:
                    nueva_res.respuesta_diagrama = valor
                    nueva_res.respuesta = ""
                else:
                    nueva_res.respuesta = valor
                    
                session.add(nueva_res)

            resolucion.estado = "Entregado"
            resolucion.fechaEntrega = datetime.now()
            
            
            asignacion = session.exec(
                sqlmodel.select(EstudianteTarea).where(
                    (EstudianteTarea.id_tarea == self.tarea_id) &
                    (EstudianteTarea.id_estudiante == usuario.id_usuario)
                )
            ).first()
            if asignacion:
                asignacion.estado = "completado"
                session.add(asignacion)
                
            
            from ..models.usuarios import Notificacion
            
            tarea_db = session.exec(sqlmodel.select(Tarea).where(Tarea.id_tarea == self.tarea_id)).first()
            if tarea_db and tarea_db.docente_id:
                notif = Notificacion(
                    remitente_id=usuario.id_usuario,
                    destinatario_id=tarea_db.docente_id,
                    titulo=f"Nueva entrega: {tarea_db.titulo}",
                    mensaje=f"El estudiante {usuario.nombreUsuario} ha entregado la tarea '{tarea_db.titulo}'.",
                    leida=False,
                    fecha=datetime.now()
                )
                session.add(notif)
                
            session.commit()

        self.timer_running = False
        
        msg = "¡Tiempo finalizado! Tus respuestas se han guardado." if timeout else "Tarea enviada correctamente."
        return [
            rx.toast.success(msg, position="bottom-right"),
            rx.redirect("/mis-tareas-estudiante")
        ]
