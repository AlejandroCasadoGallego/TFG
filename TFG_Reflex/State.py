import reflex as rx
import sqlmodel
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

    def iniciar_sesion(self):
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()

            if usuario and usuario.contraseñaHash == self.pass_input:
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

    def crear_usuario_prueba(self):
        """Crea un administrador inicial en MySQL si la tabla está vacía."""
        with rx.session() as session:
            admin_existente = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == "admin@test.com")
            ).first()

            if not admin_existente:
                nuevo_usuario = Usuario(
                    nombreUsuario="Alejandro", 
                    correo="admin@test.com", 
                    contraseñaHash="1234",
                    rol="admin"
                )
                session.add(nuevo_usuario)
                session.commit()
                
                session.refresh(nuevo_usuario) 
                
                nuevo_admin = Administrador(
                    usuario_id=nuevo_usuario.id_usuario
                )
                session.add(nuevo_admin)
                session.commit()