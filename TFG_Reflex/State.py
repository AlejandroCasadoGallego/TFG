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
    edit_nombre: str = ""
    edit_correo: str = ""
    edit_pass: str = ""
    error_edicion: str = ""

    confirm_delete_input: str = ""

    datos_perfil: dict = {}

    def iniciar_sesion(self):
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.correo == self.correo_input)
            ).first()

            if usuario and usuario.activo and usuario.contraseñaHash == self._hash_password(self.pass_input):
                self.usuario_actual = usuario.nombreUsuario
                self.usuario_rol = usuario.rol
                self.error_mensaje = ""
                return rx.redirect("/dashboard")
            elif usuario and not usuario.activo:
                self.error_mensaje = "Esta cuenta ha sido desactivada."
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
        
    def cargar_perfil(self):
        if not self.usuario_actual:
            return rx.redirect("/login")
            
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            
            if usuario:
                self.datos_perfil = {
                    "nombre": usuario.nombreUsuario,
                    "correo": usuario.correo,
                    "rol": usuario.rol,
                    "id": usuario.id_usuario
                }

    def navegar_perfil(self):
        return rx.redirect("/perfil")
    
    def preparar_edicion(self):
        self.edit_nombre = self.datos_perfil.get("nombre", "")
        self.edit_correo = self.datos_perfil.get("correo", "")
        self.edit_pass = ""
        self.error_edicion = ""
        return rx.redirect("/editar-perfil")

    def guardar_cambios_perfil(self):
        """Valida y guarda los cambios del usuario."""
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.id_usuario == self.datos_perfil["id"])
            ).first()

            if not usuario:
                return self.cerrar_sesion()

            if not self.edit_nombre.strip():
                self.error_edicion = "El nombre no puede estar vacío."
                return

            if self.edit_correo.strip() != usuario.correo:
                if not self.edit_correo.strip():
                    self.error_edicion = "El correo no puede estar vacío."
                    return
                correo_existente = session.exec(
                    sqlmodel.select(Usuario).where(Usuario.correo == self.edit_correo.strip())
                ).first()
                if correo_existente:
                    self.error_edicion = "Este correo ya está en uso."
                    return
                usuario.correo = self.edit_correo.strip()

            usuario.nombreUsuario = self.edit_nombre.strip()

            cambio_pass = False
            if self.edit_pass.strip():
                nuevo_hash = self._hash_password(self.edit_pass)
                if nuevo_hash == usuario.contraseñaHash:
                    self.error_edicion = "La nueva contraseña no puede ser igual a la actual."
                    return
                usuario.contraseñaHash = nuevo_hash
                cambio_pass = True

            session.add(usuario)
            session.commit()
            
            session.refresh(usuario)

            self.usuario_actual = usuario.nombreUsuario
            
            self.datos_perfil = {
                "nombre": usuario.nombreUsuario,
                "correo": usuario.correo,
                "rol": usuario.rol,
                "id": usuario.id_usuario
            }

            if cambio_pass:
                return self.cerrar_sesion()
            else:
                self.edit_pass = ""
                return rx.redirect("/perfil")

    def confirmar_eliminacion(self):
        if self.confirm_delete_input == "ELIMINAR":
            with rx.session() as session:
                usuario = session.exec(
                    sqlmodel.select(Usuario).where(Usuario.id_usuario == self.datos_perfil["id"])
                ).first()
                if usuario:
                    usuario.activo = False
                    session.add(usuario)
                    session.commit()
            
            self.confirm_delete_input = ""
            return self.cerrar_sesion()