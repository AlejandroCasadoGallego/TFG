import reflex as rx
import sqlmodel
import re
import time
from .base_state import BaseState
from ..models.usuarios import Usuario, Estudiante

class AuthState(BaseState):
    nombre_input: str = ""
    correo_input: str = ""
    pass_input: str = ""
    
    pass_forzado_1: str = ""
    pass_forzado_2: str = ""
    error_pass_forzado: str = ""

    _intentos_fallidos: int = 0
    _ultimo_intento: float = 0.0
    _MAX_INTENTOS: int = 5
    _COOLDOWN_SEGUNDOS: int = 60
    bloqueado_hasta: str = ""

    def _validar_password(self, password: str) -> str:
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r'[A-Z]', password):
            return "La contraseña debe contener al menos una letra mayúscula."
        if not re.search(r'[a-z]', password):
            return "La contraseña debe contener al menos una letra minúscula."
        if not re.search(r'[0-9]', password):
            return "La contraseña debe contener al menos un número."
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            return "La contraseña debe contener al menos un símbolo (ej: !@#$%)."
        return ""

    def handle_key_login(self, key: str):
        if key == "Enter":
            return self.iniciar_sesion()

    def handle_key_registro(self, key: str):
        if key == "Enter":
            return self.registrar_usuario()

    def handle_key_forzado(self, key: str):
        if key == "Enter":
            return self.guardar_pass_forzado()

    def iniciar_sesion(self, form_data: dict = None):
        ahora = time.time()

        if self._intentos_fallidos >= self._MAX_INTENTOS:
            tiempo_restante = self._COOLDOWN_SEGUNDOS - (ahora - self._ultimo_intento)
            if tiempo_restante > 0:
                segundos = int(tiempo_restante)
                self.bloqueado_hasta = f"Demasiados intentos. Espera {segundos}s."
                self.error_mensaje = self.bloqueado_hasta
                return
            else:
                self._intentos_fallidos = 0
                self.bloqueado_hasta = ""

        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()

            if usuario and usuario.activo and usuario.contraseñaHash == self._hash_password(self.pass_input):
                self._intentos_fallidos = 0
                self.bloqueado_hasta = ""
                self.usuario_actual = usuario.nombreUsuario
                self.usuario_rol = usuario.rol
                self.error_mensaje = ""
                if getattr(usuario, 'debe_cambiar_pass', False):
                    return rx.redirect("/primer-acceso")
                return rx.redirect("/dashboard")
            elif usuario and not usuario.activo:
                self.error_mensaje = "Esta cuenta ha sido desactivada."
            else:
                self._intentos_fallidos += 1
                self._ultimo_intento = ahora
                intentos_restantes = self._MAX_INTENTOS - self._intentos_fallidos
                if intentos_restantes > 0:
                    self.error_mensaje = f"Credenciales incorrectas. Te quedan {intentos_restantes} intentos."
                else:
                    self.bloqueado_hasta = f"Demasiados intentos. Espera {self._COOLDOWN_SEGUNDOS}s."
                    self.error_mensaje = self.bloqueado_hasta

    def registrar_usuario(self, form_data: dict = None):
        with rx.session() as session:
            if not self.correo_input or not self.pass_input or not self.nombre_input:
                self.error_mensaje = "Todos los campos son obligatorios."
                return

            error_pass = self._validar_password(self.pass_input)
            if error_pass:
                self.error_mensaje = error_pass
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

    def guardar_pass_forzado(self, form_data: dict = None):
        if not self.pass_forzado_1 or not self.pass_forzado_2:
            self.error_pass_forzado = "Por favor, rellena ambos campos."
            return
            
        if self.pass_forzado_1 != self.pass_forzado_2:
            self.error_pass_forzado = "Las contraseñas no coinciden."
            return

        error_pass = self._validar_password(self.pass_forzado_1)
        if error_pass:
            self.error_pass_forzado = error_pass
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