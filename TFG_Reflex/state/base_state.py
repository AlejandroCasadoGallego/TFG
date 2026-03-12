import reflex as rx
import hashlib

class BaseState(rx.State):
    usuario_actual: str = ""
    usuario_rol: str = ""
    error_mensaje: str = ""

    def cerrar_sesion(self):
        self.usuario_actual = ""
        self.usuario_rol = ""
        return rx.redirect("/")

    def check_login(self):
        if not self.usuario_actual:
            return rx.redirect("/")
    
    def _hash_password(self, password: str) -> str:
        if not password:
            return ""
        return hashlib.sha256(password.encode()).hexdigest()

    def navegar_perfil(self):
        return rx.redirect("/perfil")