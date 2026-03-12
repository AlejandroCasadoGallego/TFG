import reflex as rx
import hashlib

class BaseState(rx.State):
    """Estado base del que heredan todos los demás. Maneja la sesión global."""
    usuario_actual: str = ""
    usuario_rol: str = ""
    error_mensaje: str = ""

    def cerrar_sesion(self):
        """Limpia la sesión y vuelve al login."""
        self.usuario_actual = ""
        self.usuario_rol = ""
        return rx.redirect("/")

    def check_login(self):
        """Protección de ruta: si no hay usuario, rebota al login."""
        if not self.usuario_actual:
            return rx.redirect("/")
    
    def _hash_password(self, password: str) -> str:
        """Función privada para convertir texto plano en un hash SHA-256."""
        if not password:
            return ""
        return hashlib.sha256(password.encode()).hexdigest()

    def navegar_perfil(self):
        return rx.redirect("/perfil")