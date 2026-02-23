import reflex as rx
import sqlmodel
import hashlib
from .models.usuarios import Usuario, Administrador, Docente, Estudiante, EstudianteGrupo, Grupos
from .models.tarea import Pregunta, Tarea, Ejercicio, PruebaEvaluacion
from .models.patrones import PatronDiseño
from .models.evaluacion import ResolucionTarea, RespuestaPregunta

class State(rx.State):
    correo_input: str = ""
    pass_input: str = ""
    error_mensaje: str = ""
    usuario_actual: str = ""
    usuario_rol: str = ""
    
    nombre_input: str = ""
    correo_input: str = ""
    pass_input: str = ""
    rol_input: str = "estudiante"
    error_mensaje: str = ""
    usuario_actual: str = ""
    usuario_rol: str = ""

    def iniciar_sesion(self):
        """Comprueba las credenciales comparando el hash de la entrada con la DB."""
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()

            if usuario and usuario.contraseñaHash == self._hash_password(self.pass_input):
                self.usuario_actual = usuario.nombreUsuario
                self.usuario_rol = usuario.rol
                self.error_mensaje = ""
                return rx.redirect("/dashboard")
            else:
                self.error_mensaje = "Credenciales incorrectas."

    def cerrar_sesion(self):
        """Limpia la sesión y vuelve al login."""
        self.usuario_actual = ""
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
    
    def registrar_usuario(self):
        """Crea un nuevo usuario con la contraseña ya hasheada."""
        with rx.session() as session:
            if not self.correo_input or not self.pass_input or not self.nombre_input:
                self.error_mensaje = "Todos los campos son obligatorios."
                return

            existente = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()
            
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