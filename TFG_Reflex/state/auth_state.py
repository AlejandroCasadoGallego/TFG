import reflex as rx
import sqlmodel
from .base_state import BaseState
from ..models.usuarios import Usuario, Estudiante

class AuthState(BaseState):
    """Maneja la autenticación, registro y cambios de contraseña forzados."""
    nombre_input: str = ""
    correo_input: str = ""
    pass_input: str = ""
    
    pass_forzado_1: str = ""
    pass_forzado_2: str = ""
    error_pass_forzado: str = ""

    def iniciar_sesion(self):
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()

            if usuario and usuario.activo and usuario.contraseñaHash == self._hash_password(self.pass_input):
                self.usuario_actual = usuario.nombreUsuario
                self.usuario_rol = usuario.rol
                self.error_mensaje = ""
                if getattr(usuario, 'debe_cambiar_pass', False):
                    return rx.redirect("/primer-acceso")
                return rx.redirect("/dashboard")
            elif usuario and not usuario.activo:
                self.error_mensaje = "Esta cuenta ha sido desactivada."
            else:
                self.error_mensaje = "Credenciales incorrectas."

    def registrar_usuario(self):
        with rx.session() as session:
            if not self.correo_input or not self.pass_input or not self.nombre_input:
                self.error_mensaje = "Todos los campos son obligatorios."
                return

            existente = session.exec(sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)).first()
            if existente:
                self.error_mensaje = "Este correo ya está registrado."
                return

            nuevo_usuario = Usuario(
                nombreUsuario=self.nombre_input,
                correo=self.correo_input,
                contraseñaHash=self._hash_password(self.pass_input),
                rol="estudiante"
            )
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)

            session.add(Estudiante(usuario_id=nuevo_usuario.id_usuario))
            session.commit()
            
            self.error_mensaje = ""
            return rx.redirect("/login")

    def guardar_pass_forzado(self):
        if not self.pass_forzado_1 or not self.pass_forzado_2:
            self.error_pass_forzado = "Por favor, rellena ambos campos."
            return
            
        if self.pass_forzado_1 != self.pass_forzado_2:
            self.error_pass_forzado = "Las contraseñas no coinciden."
            return

        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if usuario:
                nuevo_hash = self._hash_password(self.pass_forzado_1)
                if nuevo_hash == usuario.contraseñaHash:
                    self.error_pass_forzado = "Debes elegir una contraseña diferente a la temporal."
                    return
                
                usuario.contraseñaHash = nuevo_hash
                usuario.debe_cambiar_pass = False
                session.add(usuario)
                session.commit()
                
                self.pass_forzado_1 = ""
                self.pass_forzado_2 = ""
                self.error_pass_forzado = ""
                return rx.redirect("/dashboard")