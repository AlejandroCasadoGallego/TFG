import reflex as rx
import sqlmodel
from typing import List
from datetime import datetime
from .base_state import BaseState


class EstudianteDestinatarioUI(rx.Base):
    id_estudiante: str = ""
    nombre: str = ""
    correo: str = ""


class MensajesState(BaseState):
    estudiantes_disponibles: List[EstudianteDestinatarioUI] = []
    busqueda_estudiante: str = ""

    destinatario_seleccionado: str = ""
    destinatario_nombre: str = ""
    titulo_mensaje: str = ""
    cuerpo_mensaje: str = ""

    mensajes_enviados: list[dict] = []

    def cargar_mensajes(self):
        if not self.usuario_actual:
            return

        with rx.session() as session:
            from ..models.usuarios import Usuario, Notificacion

            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not profesor:
                return

            estudiantes = session.exec(
                sqlmodel.select(Usuario).where(Usuario.rol == "estudiante")
            ).all()

            self.estudiantes_disponibles = [
                EstudianteDestinatarioUI(
                    id_estudiante=str(est.id_usuario),
                    nombre=est.nombreUsuario,
                    correo=est.correo,
                )
                for est in estudiantes
            ]

            mensajes = session.exec(
                sqlmodel.select(Notificacion)
                .where(Notificacion.remitente_id == profesor.id_usuario)
                .order_by(Notificacion.fecha.desc())
            ).all()

            self.mensajes_enviados = []
            for m in mensajes:
                dest = session.exec(
                    sqlmodel.select(Usuario).where(Usuario.id_usuario == m.destinatario_id)
                ).first()
                self.mensajes_enviados.append({
                    "id": m.id_notificacion,
                    "destinatario": dest.nombreUsuario if dest else "Desconocido",
                    "titulo": m.titulo,
                    "mensaje": m.mensaje,
                    "fecha": m.fecha.strftime("%d/%m/%Y %H:%M"),
                    "leida": m.leida,
                })

    @rx.var
    def estudiantes_filtrados(self) -> List[EstudianteDestinatarioUI]:
        if not self.busqueda_estudiante:
            return self.estudiantes_disponibles
        busqueda = self.busqueda_estudiante.lower()
        return [e for e in self.estudiantes_disponibles if busqueda in e.nombre.lower() or busqueda in e.correo.lower()]

    def seleccionar_destinatario(self, id_est: str, nombre: str):
        self.destinatario_seleccionado = id_est
        self.destinatario_nombre = nombre

    def enviar_mensaje(self):
        if not self.destinatario_seleccionado:
            return rx.toast.error("Selecciona un estudiante destinatario.", position="bottom-right")
        if not self.titulo_mensaje.strip():
            return rx.toast.error("El título del mensaje no puede estar vacío.", position="bottom-right")
        if not self.cuerpo_mensaje.strip():
            return rx.toast.error("El cuerpo del mensaje no puede estar vacío.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Usuario, Notificacion

            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not profesor:
                return

            nueva_notif = Notificacion(
                remitente_id=profesor.id_usuario,
                destinatario_id=int(self.destinatario_seleccionado),
                titulo=self.titulo_mensaje.strip(),
                mensaje=self.cuerpo_mensaje.strip(),
                leida=False,
                fecha=datetime.now(),
            )
            session.add(nueva_notif)
            session.commit()

        self.titulo_mensaje = ""
        self.cuerpo_mensaje = ""
        self.destinatario_seleccionado = ""
        self.destinatario_nombre = ""
        self.busqueda_estudiante = ""

        self.cargar_mensajes()
        return rx.toast.success("Mensaje enviado correctamente.", position="bottom-right")
