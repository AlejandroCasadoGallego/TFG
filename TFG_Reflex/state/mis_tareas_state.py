import reflex as rx
import sqlmodel
from typing import List
from .base_state import BaseState

class TareaUI(rx.Base):
    id_tarea: str
    titulo: str
    descripcion: str
    fechas: str
    grupo: str

class PreguntaDetalleUI(rx.Base):
    numero: str = ""
    enunciado: str = ""
    tipo: str = ""
    opciones: List[str] = []
    respuesta_correcta: str = ""

class EstudianteAsignadoUI(rx.Base):
    id_estudiante: str = ""
    nombre: str = ""
    correo: str = ""
    estado: str = ""
    ha_entregado: bool = False

class TareaDetalleUI(rx.Base):
    id_tarea: str = ""
    titulo: str = ""
    descripcion: str = ""
    enunciado: str = ""
    fechas: str = ""
    grupo: str = ""
    tipo: str = ""
    dificultad: str = ""
    tipo_entrada: str = ""
    permite_reintentos: str = ""
    tiempo_limite: str = ""
    total_preguntas: str = "0"
    total_estudiantes: str = "0"

class MisTareasState(BaseState):
    tareas: List[TareaUI] = []
    tarea_detalle: TareaDetalleUI = TareaDetalleUI()
    preguntas_detalle: List[PreguntaDetalleUI] = []
    estudiantes_detalle: List[EstudianteAsignadoUI] = []
    error_detalle: bool = False

    modal_eliminar_abierto: bool = False
    tarea_a_eliminar_id: int = -1
    tarea_a_eliminar_titulo: str = ""
    confirm_delete_input: str = ""

    def cargar_tareas(self):
        if not self.usuario_actual:
            return

        with rx.session() as session:
            from ..models.usuarios import Usuario, Grupos
            from ..models.tarea import Tarea

            profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not profesor:
                return

            statement = sqlmodel.select(Tarea).where(Tarea.docente_id == profesor.id_usuario).order_by(Tarea.fechaInicio.desc())
            resultados = session.exec(statement).all()

            lista_tareas = []
            for t in resultados:
                nombre_grupo = "Asignación Individual"
                if t.grupo_id:
                    grupo = session.exec(sqlmodel.select(Grupos).where(Grupos.id_grupo == t.grupo_id)).first()
                    if grupo:
                        nombre_grupo = f"Grupo: {grupo.nombre}"

                lista_tareas.append(TareaUI(
                    id_tarea=str(t.id_tarea),
                    titulo=t.titulo,
                    descripcion=t.descripcion if t.descripcion else "Sin descripción",
                    fechas=f"{t.fechaInicio.strftime('%d/%m/%Y')} - {t.fechaFin.strftime('%d/%m/%Y')}",
                    grupo=nombre_grupo
                ))
            
            self.tareas = lista_tareas

    def ver_detalles(self, id_tarea: str):
        return rx.redirect(f"/tarea/{id_tarea}")

    def abrir_modal_eliminar(self, id_tarea: str, titulo: str):
        self.tarea_a_eliminar_id = int(id_tarea)
        self.tarea_a_eliminar_titulo = titulo
        self.confirm_delete_input = ""
        self.modal_eliminar_abierto = True

    def cambiar_estado_modal_eliminar(self, valor: bool):
        self.modal_eliminar_abierto = valor
        if not valor:
            self.tarea_a_eliminar_id = -1
            self.tarea_a_eliminar_titulo = ""
            self.confirm_delete_input = ""

    def set_confirm_delete_input(self, valor: str):
        self.confirm_delete_input = valor

    def confirmar_eliminacion_tarea(self):
        if self.confirm_delete_input != "ELIMINAR":
            return rx.toast.error("Escribe ELIMINAR para confirmar.", position="bottom-right")

        if self.tarea_a_eliminar_id < 0:
            return rx.toast.error("No se ha seleccionado ninguna tarea.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Usuario
            from ..models.tarea import Tarea, Pregunta, EstudianteTarea, Ejercicio, PruebaEvaluacion
            from ..models.evaluacion import ResolucionTarea, RespuestaPregunta

            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not profesor:
                return rx.toast.error("No se ha podido identificar al docente.", position="bottom-right")

            tarea = session.exec(
                sqlmodel.select(Tarea).where(
                    (Tarea.id_tarea == self.tarea_a_eliminar_id) &
                    (Tarea.docente_id == profesor.id_usuario)
                )
            ).first()
            if not tarea:
                self.cambiar_estado_modal_eliminar(False)
                self.cargar_tareas()
                return rx.toast.error("La tarea no existe o no tienes permiso para eliminarla.", position="bottom-right")

            preguntas = session.exec(
                sqlmodel.select(Pregunta).where(Pregunta.tarea_id == tarea.id_tarea)
            ).all()
            for pregunta in preguntas:
                respuestas = session.exec(
                    sqlmodel.select(RespuestaPregunta).where(RespuestaPregunta.pregunta_id == pregunta.id)
                ).all()
                for respuesta in respuestas:
                    session.delete(respuesta)

            resoluciones = session.exec(
                sqlmodel.select(ResolucionTarea).where(ResolucionTarea.tarea_id == tarea.id_tarea)
            ).all()
            for resolucion in resoluciones:
                session.delete(resolucion)

            asignaciones = session.exec(
                sqlmodel.select(EstudianteTarea).where(EstudianteTarea.id_tarea == tarea.id_tarea)
            ).all()
            for asignacion in asignaciones:
                session.delete(asignacion)

            ejercicio = session.exec(
                sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)
            ).first()
            if ejercicio:
                session.delete(ejercicio)

            prueba = session.exec(
                sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == tarea.id_tarea)
            ).first()
            if prueba:
                session.delete(prueba)

            for pregunta in preguntas:
                session.delete(pregunta)

            session.delete(tarea)
            session.commit()

        self.cambiar_estado_modal_eliminar(False)
        self.cargar_tareas()
        return rx.toast.success("Tarea eliminada correctamente.", position="bottom-right")

    def cargar_detalle_tarea(self):
        id_url = self.router.page.params.get("id_tarea", "")
        self.error_detalle = False
        self.tarea_detalle = TareaDetalleUI()
        self.preguntas_detalle = []
        self.estudiantes_detalle = []

        if not id_url:
            self.error_detalle = True
            return

        try:
            id_tarea = int(id_url)
        except ValueError:
            self.error_detalle = True
            return

        with rx.session() as session:
            from ..models.usuarios import Usuario, Grupos
            from ..models.tarea import Tarea, Pregunta, EstudianteTarea, Ejercicio, PruebaEvaluacion

            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not profesor:
                self.error_detalle = True
                return

            tarea = session.exec(
                sqlmodel.select(Tarea).where(
                    (Tarea.id_tarea == id_tarea) &
                    (Tarea.docente_id == profesor.id_usuario)
                )
            ).first()
            if not tarea:
                self.error_detalle = True
                return

            nombre_grupo = "Asignación individual"
            if tarea.grupo_id:
                grupo = session.exec(sqlmodel.select(Grupos).where(Grupos.id_grupo == tarea.grupo_id)).first()
                if grupo:
                    nombre_grupo = f"Grupo: {grupo.nombre}"

            ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first()
            prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == tarea.id_tarea)).first()

            tipo = "Ejercicio" if ejercicio else "Prueba" if prueba else "Tarea"
            dificultad = ejercicio.nivelDificultad.capitalize() if ejercicio else "No aplica"
            tipo_entrada = ejercicio.tipoEntrada if ejercicio else "No aplica"
            permite_reintentos = "Sí" if ejercicio and ejercicio.permiteReintentos else "No"
            tiempo_limite = f"{prueba.tiempoLimite} minutos" if prueba else "Sin límite"

            preguntas = session.exec(
                sqlmodel.select(Pregunta)
                .where(Pregunta.tarea_id == tarea.id_tarea)
                .order_by(Pregunta.id)
            ).all()

            estudiantes = session.exec(
                sqlmodel.select(Usuario, EstudianteTarea)
                .join(EstudianteTarea, Usuario.id_usuario == EstudianteTarea.id_estudiante)
                .where(EstudianteTarea.id_tarea == tarea.id_tarea)
                .order_by(Usuario.nombreUsuario)
            ).all()

            self.tarea_detalle = TareaDetalleUI(
                id_tarea=str(tarea.id_tarea),
                titulo=tarea.titulo,
                descripcion=tarea.descripcion if tarea.descripcion else "Sin descripción",
                enunciado=tarea.enunciado if tarea.enunciado else "",
                fechas=f"{tarea.fechaInicio.strftime('%d/%m/%Y %H:%M')} - {tarea.fechaFin.strftime('%d/%m/%Y %H:%M')}",
                grupo=nombre_grupo,
                tipo=tipo,
                dificultad=dificultad,
                tipo_entrada=tipo_entrada,
                permite_reintentos=permite_reintentos,
                tiempo_limite=tiempo_limite,
                total_preguntas=str(len(preguntas)),
                total_estudiantes=str(len(estudiantes)),
            )

            lista_preguntas_detalle = []
            for index, pregunta in enumerate(preguntas):
                opciones = [opcion for opcion in (pregunta.opciones or []) if opcion]
                resp_corr = pregunta.respuestaCorrecta if pregunta.respuestaCorrecta else ""
                if pregunta.tipo == "Test" and resp_corr.isdigit():
                    idx = int(resp_corr) - 1
                    if 0 <= idx < len(opciones):
                        resp_corr = opciones[idx]
                
                lista_preguntas_detalle.append(
                    PreguntaDetalleUI(
                        numero=str(index + 1),
                        enunciado=pregunta.enunciado if pregunta.enunciado else "Sin enunciado",
                        tipo=pregunta.tipo,
                        opciones=opciones,
                        respuesta_correcta=resp_corr,
                    )
                )
            
            self.preguntas_detalle = lista_preguntas_detalle

            self.estudiantes_detalle = [
                EstudianteAsignadoUI(
                    id_estudiante=str(usuario.id_usuario),
                    nombre=usuario.nombreUsuario,
                    correo=usuario.correo,
                    estado=asignacion.estado.capitalize(),
                    ha_entregado=asignacion.estado.lower() in ["entregada", "completada", "completado", "entregado"],
                )
                for usuario, asignacion in estudiantes
            ]
