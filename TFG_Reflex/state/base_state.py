import reflex as rx
import hashlib
import sqlmodel

class BaseState(rx.State):
    usuario_actual: str = ""
    usuario_rol: str = ""
    error_mensaje: str = ""
    notificaciones_sin_leer: int = 0
    lista_notificaciones: list[dict] = []

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
                
                self.lista_notificaciones = [
                    {
                        "id": n.id_notificacion,
                        "titulo": n.titulo,
                        "mensaje": n.mensaje,
                        "leida": n.leida,
                        "fecha": n.fecha.strftime("%d/%m/%Y %H:%M")
                    } for n in notifs
                ]
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