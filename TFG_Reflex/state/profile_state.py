import reflex as rx
import sqlmodel
from .base_state import BaseState
from ..models.usuarios import Usuario

class ProfileState(BaseState):
    """Maneja la vista y edición del perfil del usuario."""
    datos_perfil: dict = {}
    edit_nombre: str = ""
    edit_correo: str = ""
    edit_pass: str = ""
    error_edicion: str = ""
    confirm_delete_input: str = ""

    def cargar_perfil(self):
        if not self.usuario_actual:
            return rx.redirect("/login")
            
        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            if usuario:
                self.datos_perfil = {
                    "nombre": usuario.nombreUsuario,
                    "correo": usuario.correo,
                    "rol": usuario.rol,
                    "id": usuario.id_usuario
                }

    def preparar_edicion(self):
        self.edit_nombre = self.datos_perfil.get("nombre", "")
        self.edit_correo = self.datos_perfil.get("correo", "")
        self.edit_pass = ""
        self.error_edicion = ""
        return rx.redirect("/editar-perfil")

    def guardar_cambios_perfil(self):
        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.id_usuario == self.datos_perfil["id"])).first()
            if not usuario:
                return self.cerrar_sesion()

            if not self.edit_nombre.strip():
                self.error_edicion = "El nombre no puede estar vacío."
                return

            if self.edit_correo.strip() != usuario.correo:
                if not self.edit_correo.strip():
                    self.error_edicion = "El correo no puede estar vacío."
                    return
                correo_existente = session.exec(sqlmodel.select(Usuario).where(Usuario.correo == self.edit_correo.strip())).first()
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
                usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.id_usuario == self.datos_perfil["id"])).first()
                if usuario:
                    usuario.activo = False
                    session.add(usuario)
                    session.commit()
            
            self.confirm_delete_input = ""
            return self.cerrar_sesion()