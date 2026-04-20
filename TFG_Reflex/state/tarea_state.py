import reflex as rx
import sqlmodel
from datetime import datetime, timedelta
from typing import List, Dict
from .base_state import BaseState

class PreguntaUI(rx.Base):
    enunciado: str = ""
    tipo: str = "Desarrollo"
    opcion1: str = ""
    opcion2: str = ""
    opcion3: str = ""
    opcion4: str = ""
    correcta: str = ""

class TareaState(BaseState):
    editando_tarea_id: int = -1
    error_edicion: str = ""
    tipo_tarea: str = "Ejercicio"
    titulo: str = ""
    descripcion: str = ""
    fecha_inicio: str = ""
    fecha_fin: str = ""
    enunciado: str = ""
    
    nivel_dificultad: str = "medio"
    permite_reintentos: bool = True
    
    tiempo_limite: str = "60"
    
    tipo_asignacion: str = "Grupo"
    grupo_seleccionado: str = ""
    busqueda_estudiante: str = ""
    estudiantes_seleccionados: List[str] = []
    
    mis_grupos_options: List[Dict[str, str]] = []
    todos_estudiantes: List[str] = []
    
    preguntas: List[PreguntaUI] = [PreguntaUI()]

    def cargar_datos_formulario(self):
        if not self.usuario_actual:
            return
            
        self.editando_tarea_id = -1
        self.error_edicion = ""
        self.limpiar_formulario()

        with rx.session() as session:
            self.cargar_opciones_asignacion(session)

    def cargar_opciones_asignacion(self, session):
        from ..models.usuarios import Usuario, Grupos

        profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
        if profesor:
            grupos = session.exec(sqlmodel.select(Grupos).where(Grupos.docente_id == profesor.id_usuario)).all()
            self.mis_grupos_options = [{"id": str(g.id_grupo), "nombre": g.nombre} for g in grupos]
        else:
            self.mis_grupos_options = []

        estudiantes = session.exec(sqlmodel.select(Usuario).where(Usuario.rol == "estudiante")).all()
        self.todos_estudiantes = [e.nombreUsuario for e in estudiantes]

    @rx.var
    def estudiantes_filtrados(self) -> List[str]:
        if not self.busqueda_estudiante:
            return self.todos_estudiantes
        return [e for e in self.todos_estudiantes if self.busqueda_estudiante.lower() in e.lower()]
    
    @rx.var
    def mis_grupos_nombres(self) -> List[str]:
        return [g["nombre"] for g in self.mis_grupos_options]

    @rx.var
    def grupo_seleccionado_nombre(self) -> str:
        for grupo in self.mis_grupos_options:
            if grupo["id"] == self.grupo_seleccionado:
                return grupo["nombre"]
        return ""

    def toggle_estudiante(self, nombre: str):
        if nombre in self.estudiantes_seleccionados:
            self.estudiantes_seleccionados.remove(nombre)
        else:
            self.estudiantes_seleccionados.append(nombre)

    def set_grupo_por_nombre(self, nombre_seleccionado: str):
        for grupo in self.mis_grupos_options:
            if grupo["nombre"] == nombre_seleccionado:
                self.grupo_seleccionado = grupo["id"]
                break

    def set_titulo(self, valor: str):
        self.titulo = valor

    def set_descripcion(self, valor: str):
        self.descripcion = valor

    def set_enunciado(self, valor: str):
        self.enunciado = valor

    def set_fecha_inicio(self, valor: str):
        self.fecha_inicio = valor

    def set_fecha_fin(self, valor: str):
        self.fecha_fin = valor

    def set_nivel_dificultad(self, valor: str):
        self.nivel_dificultad = valor

    def set_permite_reintentos(self, valor: bool):
        self.permite_reintentos = valor

    def set_tipo_asignacion(self, valor: str):
        self.tipo_asignacion = valor

    def set_busqueda_estudiante(self, valor: str):
        self.busqueda_estudiante = valor

    def parse_fecha(self, fecha_str: str) -> datetime:
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            return datetime.now()
            
    def set_tipo_tarea(self, valor: str):
        self.tipo_tarea = valor
        if valor == "Ejercicio":
            if len(self.preguntas) > 1:
                self.preguntas = self.preguntas[:1]

    def agregar_pregunta(self):
        self.preguntas.append(PreguntaUI())

    def eliminar_pregunta(self, index: int):
        if len(self.preguntas) > 1:
            self.preguntas.pop(index)

    def update_pregunta(self, index: int, field: str, value: str):
        temp_preguntas = self.preguntas.copy()
        dict_pregunta = temp_preguntas[index].dict()
        dict_pregunta[field] = value
        temp_preguntas[index] = PreguntaUI(**dict_pregunta)
        self.preguntas = temp_preguntas

    def crear_notificaciones_tarea(self, session, profesor_id: int, estudiantes_ids: List[int], titulo: str, fecha_fin: datetime, es_actualizacion: bool = False):
        from ..models.usuarios import Notificacion

        ids_unicos = list(dict.fromkeys(estudiantes_ids))
        titulo_notificacion = f"Nueva Tarea: {titulo}" if not es_actualizacion else f"Nueva asignación: {titulo}"
        mensaje = (
            f"Tienes una nueva tarea asignada. Tipo: {self.tipo_tarea.capitalize()}.\n"
            f"Fecha límite: {fecha_fin.strftime('%d/%m/%Y %H:%M')}"
        )

        if es_actualizacion:
            mensaje = (
                f"Tu profesor te ha asignado a la tarea '{titulo}'.\n"
                f"Tipo: {self.tipo_tarea.capitalize()}.\n"
                f"Fecha límite: {fecha_fin.strftime('%d/%m/%Y %H:%M')}"
            )

        for id_estudiante in ids_unicos:
            session.add(Notificacion(
                remitente_id=profesor_id,
                destinatario_id=id_estudiante,
                titulo=titulo_notificacion,
                mensaje=mensaje,
                leida=False,
            ))

    def crear_tarea(self):
        if not self.titulo:
            return rx.toast.error("El título es obligatorio.", position="bottom-right")
            
        if self.tipo_tarea.lower() == "prueba":
            if not self.fecha_inicio or not self.fecha_fin:
                return rx.toast.error("Debes establecer las fechas de inicio y fin para la prueba.", position="bottom-right")
                
        if self.tipo_asignacion.lower() == "grupo" and not self.grupo_seleccionado:
            return rx.toast.error("Debes seleccionar un grupo.", position="bottom-right")
        if self.tipo_asignacion.lower() == "estudiantes" and not self.estudiantes_seleccionados:
            return rx.toast.error("Debes seleccionar al menos un estudiante.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Usuario, Grupos, EstudianteGrupo
            from ..models.tarea import Tarea, Ejercicio, PruebaEvaluacion, EstudianteTarea, Pregunta
            
            profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not profesor:
                return rx.toast.error("No se ha podido identificar al docente.", position="bottom-right")
            
            if self.tipo_tarea.lower() == "ejercicio":
                inicio_real = datetime.now()
                fin_real = datetime(9999, 12, 31)
            else:
                inicio_real = self.parse_fecha(self.fecha_inicio)
                fin_real = self.parse_fecha(self.fecha_fin)

            nueva_tarea = Tarea(
                titulo=self.titulo,
                descripcion=self.descripcion,
                enunciado=self.enunciado,
                fechaInicio=inicio_real,
                fechaFin=fin_real,
                docente_id=profesor.id_usuario,
                grupo_id=int(self.grupo_seleccionado) if self.tipo_asignacion.lower() == "grupo" else None
            )
            session.add(nueva_tarea)
            session.commit()
            session.refresh(nueva_tarea)
            
            if self.tipo_tarea.lower() == "ejercicio":
                nuevo_ejercicio = Ejercicio(
                    tarea_id=nueva_tarea.id_tarea,
                    nivelDificultad=self.nivel_dificultad,
                    tipoEntrada=self.preguntas[0].tipo,
                    permiteReintentos=self.permite_reintentos
                )
                session.add(nuevo_ejercicio)
            else:
                diferencia = fin_real - inicio_real
                minutos_calculados = int(diferencia.total_seconds() / 60)
                if minutos_calculados <= 0: 
                    minutos_calculados = 60
                
                nueva_prueba = PruebaEvaluacion(
                    tarea_id=nueva_tarea.id_tarea,
                    fechaInicioPrueba=inicio_real,
                    fechaCierre=fin_real,
                    tiempoLimite=minutos_calculados
                )
                session.add(nueva_prueba)

            for p in self.preguntas:
                if p.tipo == "Test":
                    opciones_finales = [p.opcion1, p.opcion2, p.opcion3, p.opcion4]
                    correcta_final = p.correcta
                else:
                    opciones_finales = []
                    correcta_final = ""

                nueva_p = Pregunta(
                    enunciado=p.enunciado,
                    tipo=p.tipo,
                    opciones=opciones_finales,
                    respuestaCorrecta=correcta_final,
                    tarea_id=nueva_tarea.id_tarea
                )
                session.add(nueva_p)

            estudiantes_ids_a_asignar = []
            if self.tipo_asignacion.lower() == "grupo":
                miembros = session.exec(sqlmodel.select(EstudianteGrupo).where(EstudianteGrupo.grupo_id == int(self.grupo_seleccionado))).all()
                estudiantes_ids_a_asignar = [m.estudiante_id for m in miembros]
            elif self.tipo_asignacion.lower() == "estudiantes":
                for nombre in self.estudiantes_seleccionados:
                    usr = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == nombre)).first()
                    if usr: estudiantes_ids_a_asignar.append(usr.id_usuario)

            estudiantes_ids_a_asignar = list(dict.fromkeys(estudiantes_ids_a_asignar))
            for est_id in estudiantes_ids_a_asignar:
                matricula_tarea = EstudianteTarea(id_estudiante=est_id, id_tarea=nueva_tarea.id_tarea, estado="pendiente")
                session.add(matricula_tarea)

            self.crear_notificaciones_tarea(
                session=session,
                profesor_id=profesor.id_usuario,
                estudiantes_ids=estudiantes_ids_a_asignar,
                titulo=self.titulo,
                fecha_fin=fin_real,
            )
                
            session.commit()
            
            self.limpiar_formulario()
            
            return [
                rx.toast.success("Tarea y preguntas creadas con éxito."),
                rx.redirect("/dashboard")
            ]

    def cargar_tarea_edicion(self):
        if not self.usuario_actual:
            return

        id_url = self.router.page.params.get("id_tarea", "")
        if not id_url:
            self.error_edicion = "No se ha indicado ninguna tarea."
            return

        try:
            id_tarea = int(id_url)
        except ValueError:
            self.error_edicion = "El identificador de la tarea no es válido."
            return

        self.limpiar_formulario()
        self.editando_tarea_id = id_tarea
        self.error_edicion = ""

        with rx.session() as session:
            from ..models.usuarios import Usuario
            from ..models.tarea import Tarea, Pregunta, EstudianteTarea, Ejercicio, PruebaEvaluacion

            self.cargar_opciones_asignacion(session)

            profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not profesor:
                self.error_edicion = "No se ha podido identificar al docente."
                return

            tarea = session.exec(
                sqlmodel.select(Tarea).where(
                    (Tarea.id_tarea == id_tarea) &
                    (Tarea.docente_id == profesor.id_usuario)
                )
            ).first()
            if not tarea:
                self.error_edicion = "La tarea no existe o no tienes permiso para editarla."
                return

            ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first()
            prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == tarea.id_tarea)).first()
            preguntas_db = session.exec(
                sqlmodel.select(Pregunta)
                .where(Pregunta.tarea_id == tarea.id_tarea)
                .order_by(Pregunta.id)
            ).all()

            self.titulo = tarea.titulo
            self.descripcion = tarea.descripcion or ""
            self.enunciado = tarea.enunciado or ""
            self.fecha_inicio = tarea.fechaInicio.strftime("%Y-%m-%dT%H:%M")
            self.fecha_fin = tarea.fechaFin.strftime("%Y-%m-%dT%H:%M")

            if ejercicio:
                self.tipo_tarea = "Ejercicio"
                self.nivel_dificultad = ejercicio.nivelDificultad
                self.permite_reintentos = ejercicio.permiteReintentos
            elif prueba:
                self.tipo_tarea = "Prueba"
                self.tiempo_limite = str(prueba.tiempoLimite)
            else:
                self.tipo_tarea = "Prueba"

            if tarea.grupo_id:
                self.tipo_asignacion = "Grupo"
                self.grupo_seleccionado = str(tarea.grupo_id)
                self.estudiantes_seleccionados = []
            else:
                self.tipo_asignacion = "Estudiantes"
                asignaciones = session.exec(
                    sqlmodel.select(Usuario.nombreUsuario)
                    .join(EstudianteTarea, Usuario.id_usuario == EstudianteTarea.id_estudiante)
                    .where(EstudianteTarea.id_tarea == tarea.id_tarea)
                ).all()
                self.estudiantes_seleccionados = list(asignaciones)

            preguntas_form = []
            for pregunta in preguntas_db:
                opciones = list(pregunta.opciones or [])
                while len(opciones) < 4:
                    opciones.append("")

                preguntas_form.append(PreguntaUI(
                    enunciado=pregunta.enunciado,
                    tipo=pregunta.tipo,
                    opcion1=opciones[0],
                    opcion2=opciones[1],
                    opcion3=opciones[2],
                    opcion4=opciones[3],
                    correcta=pregunta.respuestaCorrecta or "",
                ))

            self.preguntas = preguntas_form if preguntas_form else [PreguntaUI()]

    def actualizar_tarea(self):
        if self.editando_tarea_id < 0:
            return rx.toast.error("No hay ninguna tarea cargada para editar.", position="bottom-right")

        if not self.titulo.strip():
            return rx.toast.error("El título es obligatorio.", position="bottom-right")

        if self.tipo_tarea.lower() == "prueba" and (not self.fecha_inicio or not self.fecha_fin):
            return rx.toast.error("Debes establecer las fechas de inicio y fin para la prueba.", position="bottom-right")

        if self.tipo_asignacion.lower() == "grupo" and not self.grupo_seleccionado:
            return rx.toast.error("Debes seleccionar un grupo.", position="bottom-right")

        if self.tipo_asignacion.lower() == "estudiantes" and not self.estudiantes_seleccionados:
            return rx.toast.error("Debes seleccionar al menos un estudiante.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Usuario, EstudianteGrupo
            from ..models.tarea import Tarea, Pregunta, EstudianteTarea, Ejercicio, PruebaEvaluacion
            from ..models.evaluacion import RespuestaPregunta

            profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if not profesor:
                return rx.toast.error("No se ha podido identificar al docente.", position="bottom-right")

            tarea = session.exec(
                sqlmodel.select(Tarea).where(
                    (Tarea.id_tarea == self.editando_tarea_id) &
                    (Tarea.docente_id == profesor.id_usuario)
                )
            ).first()
            if not tarea:
                return rx.toast.error("La tarea no existe o no tienes permiso para editarla.", position="bottom-right")

            if self.tipo_tarea.lower() == "ejercicio":
                inicio_real = tarea.fechaInicio
                fin_real = datetime(9999, 12, 31)
            else:
                inicio_real = self.parse_fecha(self.fecha_inicio)
                fin_real = self.parse_fecha(self.fecha_fin)

            tarea.titulo = self.titulo.strip()
            tarea.descripcion = self.descripcion.strip()
            tarea.enunciado = self.enunciado.strip()
            tarea.fechaInicio = inicio_real
            tarea.fechaFin = fin_real
            tarea.grupo_id = int(self.grupo_seleccionado) if self.tipo_asignacion.lower() == "grupo" else None
            session.add(tarea)

            ejercicio = session.exec(sqlmodel.select(Ejercicio).where(Ejercicio.tarea_id == tarea.id_tarea)).first()
            prueba = session.exec(sqlmodel.select(PruebaEvaluacion).where(PruebaEvaluacion.tarea_id == tarea.id_tarea)).first()

            if self.tipo_tarea.lower() == "ejercicio":
                if prueba:
                    session.delete(prueba)

                if not ejercicio:
                    ejercicio = Ejercicio(tarea_id=tarea.id_tarea, nivelDificultad=self.nivel_dificultad, tipoEntrada=self.preguntas[0].tipo, permiteReintentos=self.permite_reintentos)

                ejercicio.nivelDificultad = self.nivel_dificultad
                ejercicio.tipoEntrada = self.preguntas[0].tipo
                ejercicio.permiteReintentos = self.permite_reintentos
                session.add(ejercicio)
            else:
                if ejercicio:
                    session.delete(ejercicio)

                diferencia = fin_real - inicio_real
                minutos_calculados = int(diferencia.total_seconds() / 60)
                if minutos_calculados <= 0:
                    minutos_calculados = 60

                if not prueba:
                    prueba = PruebaEvaluacion(tarea_id=tarea.id_tarea, fechaInicioPrueba=inicio_real, fechaCierre=fin_real, tiempoLimite=minutos_calculados)

                prueba.fechaInicioPrueba = inicio_real
                prueba.fechaCierre = fin_real
                prueba.tiempoLimite = minutos_calculados
                session.add(prueba)

            preguntas_actuales = session.exec(sqlmodel.select(Pregunta).where(Pregunta.tarea_id == tarea.id_tarea)).all()
            for pregunta in preguntas_actuales:
                respuestas = session.exec(sqlmodel.select(RespuestaPregunta).where(RespuestaPregunta.pregunta_id == pregunta.id)).all()
                for respuesta in respuestas:
                    session.delete(respuesta)
                session.delete(pregunta)
            session.flush()

            preguntas_a_guardar = self.preguntas[:1] if self.tipo_tarea.lower() == "ejercicio" else self.preguntas
            for p in preguntas_a_guardar:
                opciones_finales = [p.opcion1, p.opcion2, p.opcion3, p.opcion4] if p.tipo == "Test" else []
                nueva_pregunta = Pregunta(
                    enunciado=p.enunciado,
                    tipo=p.tipo,
                    opciones=opciones_finales,
                    respuestaCorrecta=p.correcta if p.tipo == "Test" else "",
                    tarea_id=tarea.id_tarea,
                )
                session.add(nueva_pregunta)

            asignaciones_actuales = session.exec(sqlmodel.select(EstudianteTarea).where(EstudianteTarea.id_tarea == tarea.id_tarea)).all()
            estudiantes_ids_previos = {asignacion.id_estudiante for asignacion in asignaciones_actuales}
            for asignacion in asignaciones_actuales:
                session.delete(asignacion)
            session.flush()

            estudiantes_ids_a_asignar = []
            if self.tipo_asignacion.lower() == "grupo":
                miembros = session.exec(sqlmodel.select(EstudianteGrupo).where(EstudianteGrupo.grupo_id == int(self.grupo_seleccionado))).all()
                estudiantes_ids_a_asignar = [m.estudiante_id for m in miembros]
            else:
                for nombre in self.estudiantes_seleccionados:
                    usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == nombre)).first()
                    if usuario:
                        estudiantes_ids_a_asignar.append(usuario.id_usuario)

            estudiantes_ids_a_asignar = list(dict.fromkeys(estudiantes_ids_a_asignar))
            for id_estudiante in estudiantes_ids_a_asignar:
                session.add(EstudianteTarea(id_estudiante=id_estudiante, id_tarea=tarea.id_tarea, estado="pendiente"))

            estudiantes_ids_nuevos = [
                id_estudiante for id_estudiante in estudiantes_ids_a_asignar
                if id_estudiante not in estudiantes_ids_previos
            ]
            self.crear_notificaciones_tarea(
                session=session,
                profesor_id=profesor.id_usuario,
                estudiantes_ids=estudiantes_ids_nuevos,
                titulo=tarea.titulo,
                fecha_fin=fin_real,
                es_actualizacion=True,
            )

            session.commit()

        return [
            rx.toast.success("Tarea actualizada correctamente.", position="bottom-right"),
            rx.redirect(f"/tarea/{self.editando_tarea_id}")
        ]
        
    def limpiar_formulario(self):
        self.titulo = ""
        self.descripcion = ""
        self.enunciado = ""
        self.tipo_tarea = "Ejercicio"
        self.tipo_asignacion = "Grupo"
        self.grupo_seleccionado = ""
        self.estudiantes_seleccionados = []
        self.busqueda_estudiante = ""
        self.nivel_dificultad = "medio"
        self.permite_reintentos = True
        
        ahora = datetime.now()
        manana = ahora + timedelta(days=1)
        self.fecha_inicio = ahora.strftime("%Y-%m-%dT%H:%M")
        self.fecha_fin = manana.strftime("%Y-%m-%dT%H:%M")
        
        self.preguntas = [PreguntaUI(
            enunciado="", 
            tipo="Desarrollo", 
            opcion1="", 
            opcion2="", 
            opcion3="", 
            opcion4="", 
            correcta=""
        )]

    @rx.var
    def tiempo_limite_calculado(self) -> str:
        if not self.fecha_inicio or not self.fecha_fin:
            return "0 mins"
            
        try:
            inicio_str = self.fecha_inicio[:16]
            fin_str = self.fecha_fin[:16]
            
            inicio = datetime.strptime(inicio_str, "%Y-%m-%dT%H:%M")
            fin = datetime.strptime(fin_str, "%Y-%m-%dT%H:%M")
            
            diferencia = fin - inicio
            minutos = int(diferencia.total_seconds() / 60)
            
            if minutos <= 0:
                return "Error: Revisa las fechas"
            
            return f"{minutos} mins"
        except Exception:
            return "0 mins"
