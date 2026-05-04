import reflex as rx
import sqlmodel
from typing import List
from .base_state import BaseState

class RespuestaCorregidaUI(rx.Base):
    id_pregunta: str
    numero: str
    enunciado: str
    tipo: str
    respuesta_texto: str
    respuesta_diagrama: str
    calificacion: float
    calificacion_maxima: float
    retroalimentacion: str

class VerCorreccionState(BaseState):
    id_tarea_actual: str = ""
    
    titulo_tarea: str = ""
    descripcion_tarea: str = ""
    fecha_entrega: str = ""
    calificacion_total: float = 0.0
    calificacion_maxima_total: float = 0.0
    
    respuestas: List[RespuestaCorregidaUI] = []
    error_carga: bool = False
    
    def cargar_correccion(self):
        if not self.usuario_actual:
            return
            
        id_tarea = self.router.page.params.get("id_tarea", "")
        
        self.error_carga = False
        self.respuestas = []
        self.titulo_tarea = ""
        self.descripcion_tarea = ""
        self.fecha_entrega = ""
        self.calificacion_total = 0.0
        self.calificacion_maxima_total = 0.0
        
        if not id_tarea:
            self.error_carga = True
            return
            
        self.id_tarea_actual = id_tarea
        
        try:
            id_tarea_int = int(id_tarea)
        except ValueError:
            self.error_carga = True
            return
            
        with rx.session() as session:
            from ..models.tarea import Tarea, Pregunta
            from ..models.usuarios import Usuario
            from ..models.evaluacion import ResolucionTarea, RespuestaPregunta
            
            estudiante = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            tarea = session.exec(sqlmodel.select(Tarea).where(Tarea.id_tarea == id_tarea_int)).first()
            
            if not tarea or not estudiante:
                self.error_carga = True
                return
                
            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea)
                .where((ResolucionTarea.tarea_id == id_tarea_int) & (ResolucionTarea.estudiante_id == estudiante.id_usuario))
            ).first()
            
            if not resolucion or resolucion.estado != "corregida":
                self.error_carga = True
                return
                
            self.titulo_tarea = tarea.titulo
            self.descripcion_tarea = tarea.descripcion or "Sin descripción"
            self.fecha_entrega = resolucion.fechaEntrega.strftime("%d/%m/%Y %H:%M")
            self.calificacion_total = float(resolucion.calificacionTotal)
            
            respuestas_bd = session.exec(
                sqlmodel.select(RespuestaPregunta)
                .where(RespuestaPregunta.resolucion_id == resolucion.id)
            ).all()
            
            preguntas = session.exec(
                sqlmodel.select(Pregunta)
                .where(Pregunta.tarea_id == id_tarea_int)
                .order_by(Pregunta.id)
            ).all()
            
            lista_respuestas = []
            max_total = 0.0
            for i, pregunta in enumerate(preguntas):
                max_pregunta = float(pregunta.calificacion_maxima) if hasattr(pregunta, 'calificacion_maxima') else 10.0
                max_total += max_pregunta
                
                respuesta_alumno = next((r for r in respuestas_bd if r.pregunta_id == pregunta.id), None)
                
                respuesta_texto = respuesta_alumno.respuesta if respuesta_alumno else ""
                if pregunta.tipo == "Test" and respuesta_texto.isdigit():
                    idx = int(respuesta_texto) - 1
                    opciones = [opcion for opcion in (pregunta.opciones or []) if opcion]
                    if 0 <= idx < len(opciones):
                        respuesta_texto = opciones[idx]

                resp_diagrama = respuesta_alumno.respuesta_diagrama if respuesta_alumno and respuesta_alumno.respuesta_diagrama else ""

                lista_respuestas.append(
                    RespuestaCorregidaUI(
                        id_pregunta=str(pregunta.id),
                        numero=str(i + 1),
                        enunciado=pregunta.enunciado or "Sin enunciado",
                        tipo=pregunta.tipo,
                        respuesta_texto=respuesta_texto,
                        respuesta_diagrama=resp_diagrama,
                        calificacion=float(respuesta_alumno.calificacion) if respuesta_alumno else 0.0,
                        calificacion_maxima=max_pregunta,
                        retroalimentacion=respuesta_alumno.retroalimentacion if respuesta_alumno and respuesta_alumno.retroalimentacion else "Sin comentarios del profesor."
                    )
                )
                
            self.respuestas = lista_respuestas
            self.calificacion_maxima_total = max_total
