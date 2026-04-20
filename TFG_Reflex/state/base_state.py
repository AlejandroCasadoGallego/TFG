import reflex as rx
import hashlib
import sqlmodel
from datetime import datetime

class BaseState(rx.State):
    usuario_actual: str = ""
    usuario_rol: str = ""
    error_mensaje: str = ""
    notificaciones_sin_leer: int = 0
    lista_notificaciones: list[dict] = []

    
    modal_respuesta_abierto: bool = False
    respuesta_notif_id: int = -1
    respuesta_remitente_id: int = -1
    respuesta_remitente_nombre: str = ""
    respuesta_titulo_original: str = ""
    respuesta_texto: str = ""

    def comprobar_notificaciones(self):
        if not self.usuario_actual:
            return
        with rx.session() as session:
            from ..models.usuarios import Usuario, Notificacion
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if usuario:
                self.notificaciones_sin_leer = len(session.exec(
                    sqlmodel.select(Notificacion).where(
                        (Notificacion.destinatario_id == usuario.id_usuario) & 
                        (Notificacion.leida == False)
                    )
                ).all())

    def cerrar_sesion(self):
        self.usuario_actual = ""
        self.usuario_rol = ""
        return rx.redirect("/")

    def check_login(self):
        if not self.usuario_actual:
            return rx.redirect("/")
        self.comprobar_notificaciones()
    
    def _hash_password(self, password: str) -> str:
        if not password:
            return ""
        return hashlib.sha256(password.encode()).hexdigest()

    def navegar_perfil(self):
        return rx.redirect("/perfil")
    
    def cargar_notificaciones(self):
        if not self.usuario_actual:
            return
        with rx.session() as session:
            from ..models.usuarios import Usuario, Notificacion
            user = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if user:
                notifs = session.exec(
                    sqlmodel.select(Notificacion)
                    .where(Notificacion.destinatario_id == user.id_usuario)
                    .order_by(Notificacion.fecha.desc())
                ).all()
                
                self.lista_notificaciones = []
                for n in notifs:
                    remitente = session.exec(
                        sqlmodel.select(Usuario).where(Usuario.id_usuario == n.remitente_id)
                    ).first()
                    self.lista_notificaciones.append({
                        "id": n.id_notificacion,
                        "titulo": n.titulo,
                        "mensaje": n.mensaje,
                        "leida": n.leida,
                        "fecha": n.fecha.strftime("%d/%m/%Y %H:%M"),
                        "remitente_id": n.remitente_id,
                        "remitente_nombre": remitente.nombreUsuario if remitente else "Desconocido",
                    })
                self.comprobar_notificaciones()

    def marcar_como_leida(self, id_notif: int):
        with rx.session() as session:
            from ..models.usuarios import Notificacion
            notif = session.exec(sqlmodel.select(Notificacion).where(Notificacion.id_notificacion == id_notif)).first()
            if notif:
                notif.leida = True
                session.add(notif)
                session.commit()
                self.cargar_notificaciones()

    def eliminar_notificacion(self, id_notif: int):
        with rx.session() as session:
            from ..models.usuarios import Notificacion
            
            notif = session.exec(sqlmodel.select(Notificacion).where(Notificacion.id_notificacion == id_notif)).first()
            if notif:
                session.delete(notif)
                session.commit()
                
                self.cargar_notificaciones()
                return rx.toast.info("Notificación eliminada", position="bottom-right")

    def abrir_modal_respuesta(self, id_notif: int, remitente_id: int, remitente_nombre: str, titulo_original: str):
        self.respuesta_notif_id = id_notif
        self.respuesta_remitente_id = remitente_id
        self.respuesta_remitente_nombre = remitente_nombre
        self.respuesta_titulo_original = titulo_original
        self.respuesta_texto = ""
        self.modal_respuesta_abierto = True

    def cerrar_modal_respuesta(self, _val=None):
        self.modal_respuesta_abierto = False
        self.respuesta_texto = ""

    def enviar_respuesta(self):
        if not self.respuesta_texto.strip():
            return rx.toast.error("Escribe un mensaje de respuesta.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Usuario, Notificacion

            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            if not usuario:
                return

            nueva_notif = Notificacion(
                remitente_id=usuario.id_usuario,
                destinatario_id=self.respuesta_remitente_id,
                titulo=f"Re: {self.respuesta_titulo_original}",
                mensaje=self.respuesta_texto.strip(),
                leida=False,
                fecha=datetime.now(),
            )
            session.add(nueva_notif)
            session.commit()

        self.modal_respuesta_abierto = False
        self.respuesta_texto = ""
        self.cargar_notificaciones()
        return rx.toast.success(f"Respuesta enviada a {self.respuesta_remitente_nombre}.", position="bottom-right")
