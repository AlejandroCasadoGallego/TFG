import reflex as rx
import sqlmodel
from typing import List
from .base_state import BaseState

class RespuestaUI(rx.Base):
    id_pregunta: str
    numero: str
    enunciado: str
    tipo: str
    respuesta_texto: str
    respuesta_diagrama: str
    calificacion: float
    calificacion_maxima: float
    retroalimentacion: str = ""

class EvaluarTareaState(BaseState):
    id_tarea_actual: str = ""
    id_estudiante_actual: str = ""
    
    titulo_tarea: str = ""
    nombre_estudiante: str = ""
    fecha_entrega: str = ""
    
    respuestas: List[RespuestaUI] = []
    error_carga: bool = False
    
    def cargar_resolucion(self):
        id_tarea = self.router.page.params.get("id_tarea", "")
        id_estudiante = self.router.page.params.get("id_estudiante", "")
        
        self.error_carga = False
        self.respuestas = []
        self.titulo_tarea = ""
        self.nombre_estudiante = ""
        self.fecha_entrega = ""
        
        if not id_tarea or not id_estudiante:
            self.error_carga = True
            return
            
        self.id_tarea_actual = id_tarea
        self.id_estudiante_actual = id_estudiante
        
        try:
            id_tarea_int = int(id_tarea)
            id_estudiante_int = int(id_estudiante)
        except ValueError:
            self.error_carga = True
            return
            
        with rx.session() as session:
            from ..models.tarea import Tarea, Pregunta
            from ..models.usuarios import Usuario
            from ..models.evaluacion import ResolucionTarea, RespuestaPregunta
            
            tarea = session.exec(sqlmodel.select(Tarea).where(Tarea.id_tarea == id_tarea_int)).first()
            estudiante = session.exec(sqlmodel.select(Usuario).where(Usuario.id_usuario == id_estudiante_int)).first()
            
            if not tarea or not estudiante:
                self.error_carga = True
                return
                
            self.titulo_tarea = tarea.titulo
            self.nombre_estudiante = estudiante.nombreUsuario
            
            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea)
                .where((ResolucionTarea.tarea_id == id_tarea_int) & (ResolucionTarea.estudiante_id == id_estudiante_int))
            ).first()
            
            if not resolucion:
                self.error_carga = True
                return
                
            self.fecha_entrega = resolucion.fechaEntrega.strftime("%d/%m/%Y %H:%M")
            
            
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
            for i, pregunta in enumerate(preguntas):
                
                respuesta_alumno = next((r for r in respuestas_bd if r.pregunta_id == pregunta.id), None)
                
                respuesta_texto = respuesta_alumno.respuesta if respuesta_alumno else ""
                if pregunta.tipo == "Test" and respuesta_texto.isdigit():
                    idx = int(respuesta_texto) - 1
                    opciones = [opcion for opcion in (pregunta.opciones or []) if opcion]
                    if 0 <= idx < len(opciones):
                        respuesta_texto = opciones[idx]

                resp_diagrama = respuesta_alumno.respuesta_diagrama if respuesta_alumno and respuesta_alumno.respuesta_diagrama else ""

                lista_respuestas.append(
                    RespuestaUI(
                        id_pregunta=str(pregunta.id),
                        numero=str(i + 1),
                        enunciado=pregunta.enunciado or "Sin enunciado",
                        tipo=pregunta.tipo,
                        respuesta_texto=respuesta_texto,
                        respuesta_diagrama=resp_diagrama,
                        calificacion=float(respuesta_alumno.calificacion) if respuesta_alumno else 0.0,
                        calificacion_maxima=float(pregunta.calificacion_maxima) if hasattr(pregunta, 'calificacion_maxima') else 10.0,
                        retroalimentacion=respuesta_alumno.retroalimentacion if respuesta_alumno and respuesta_alumno.retroalimentacion else ""
                    )
                )
                
            self.respuestas = lista_respuestas

    def actualizar_calificacion(self, id_pregunta: str, valor: str):
        temp_respuestas = self.respuestas.copy()
        for i, resp in enumerate(temp_respuestas):
            if resp.id_pregunta == id_pregunta:
                try:
                    calif = float(valor)
                    dict_resp = resp.dict()
                    dict_resp["calificacion"] = calif
                    temp_respuestas[i] = RespuestaUI(**dict_resp)
                except ValueError:
                    pass
                break
        self.respuestas = temp_respuestas

    def actualizar_retroalimentacion(self, id_pregunta: str, valor: str):
        temp_respuestas = self.respuestas.copy()
        for i, resp in enumerate(temp_respuestas):
            if resp.id_pregunta == id_pregunta:
                dict_resp = resp.dict()
                dict_resp["retroalimentacion"] = valor
                temp_respuestas[i] = RespuestaUI(**dict_resp)
                break
        self.respuestas = temp_respuestas

    def calificar_tarea(self):
        for resp in self.respuestas:
            if resp.calificacion > resp.calificacion_maxima:
                return rx.toast.error(f"Error: La pregunta {resp.numero} tiene una nota de {resp.calificacion} superior al máximo permitido ({resp.calificacion_maxima}).", position="bottom-right")
            if resp.calificacion < 0:
                return rx.toast.error(f"Error: La pregunta {resp.numero} tiene una calificación negativa.", position="bottom-right")

        id_tarea_int = int(self.id_tarea_actual)
        id_estudiante_int = int(self.id_estudiante_actual)

        with rx.session() as session:
            from ..models.evaluacion import ResolucionTarea, RespuestaPregunta
            
            resolucion = session.exec(
                sqlmodel.select(ResolucionTarea)
                .where((ResolucionTarea.tarea_id == id_tarea_int) & (ResolucionTarea.estudiante_id == id_estudiante_int))
            ).first()
            
            if not resolucion:
                return rx.toast.error("Error: Resolución no encontrada.")

            total_calificacion = 0.0

            for resp_ui in self.respuestas:
                respuesta_bd = session.exec(
                    sqlmodel.select(RespuestaPregunta)
                    .where(
                        (RespuestaPregunta.resolucion_id == resolucion.id) & 
                        (RespuestaPregunta.pregunta_id == int(resp_ui.id_pregunta))
                    )
                ).first()
                
                if respuesta_bd:
                    respuesta_bd.calificacion = resp_ui.calificacion
                    respuesta_bd.retroalimentacion = resp_ui.retroalimentacion
                    session.add(respuesta_bd)
                    total_calificacion += resp_ui.calificacion

            resolucion.calificacionTotal = total_calificacion
            resolucion.estado = "corregida"
            resolucion.calificacion_liberada = False
            session.add(resolucion)

            session.commit()

        return [
            rx.toast.success("Calificación guardada. Recuerda liberarla desde el detalle de la tarea.", position="bottom-right"),
            rx.redirect(f"/tarea/{self.id_tarea_actual}")
        ]
