import reflex as rx
import sqlmodel
from .base_state import BaseState
from ..models.usuarios import Usuario, Docente, Estudiante

class AdminState(BaseState):
    total_docentes: str = "0"
    lista_docentes: list[dict[str, str]] = []
    
    new_doc_nombre: str = ""
    new_doc_correo: str = ""
    new_doc_pass: str = ""
    error_new_doc: str = ""

    total_estudiantes: str = "0"
    lista_estudiantes: list[dict[str, str]] = []

    def cargar_estadisticas_admin(self):
        if self.usuario_rol != "admin":
            return
        with rx.session() as session:
            docentes = session.exec(sqlmodel.select(Docente).join(Usuario).where(Usuario.activo == True)).all()
            self.total_docentes = str(len(docentes))

            estudiantes = session.exec(sqlmodel.select(Estudiante).join(Usuario).where(Usuario.activo == True)).all()
            self.total_estudiantes = str(len(estudiantes))

    def cargar_docentes(self):
        if self.usuario_rol != "admin":
            return rx.redirect("/dashboard")
        with rx.session() as session:
            statement = sqlmodel.select(Usuario).join(Docente).where(Usuario.id_usuario == Docente.usuario_id)
            resultados = session.exec(statement).all()
            self.lista_docentes = [{"id": str(u.id_usuario), "nombre": u.nombreUsuario, "correo": u.correo, "estado": "Activo" if u.activo else "Inactivo"} for u in resultados]

    def toggle_estado_docente(self, id_usuario_str: str):
        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.id_usuario == int(id_usuario_str))).first()
            if usuario:
                from datetime import datetime
                usuario.activo = not usuario.activo
                usuario.fecha_desactivacion = datetime.utcnow() if not usuario.activo else None
                session.add(usuario)
                session.commit()
        self.cargar_docentes()
        self.cargar_estadisticas_admin()

    def registrar_docente(self):
        with rx.session() as session:
            if not self.new_doc_nombre.strip() or not self.new_doc_correo.strip() or not self.new_doc_pass.strip():
                self.error_new_doc = "Todos los campos son obligatorios."
                return
            existente = session.exec(sqlmodel.select(Usuario).where(Usuario.correo == self.new_doc_correo.strip())).first()
            if existente:
                self.error_new_doc = "Este correo ya está registrado."
                return

            nuevo_usuario = Usuario(
                nombreUsuario=self.new_doc_nombre.strip(), correo=self.new_doc_correo.strip(),
                contraseñaHash=self._hash_password(self.new_doc_pass.strip()), rol="docente", activo=True, debe_cambiar_pass=True
            )
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)
            session.add(Docente(usuario_id=nuevo_usuario.id_usuario))
            session.commit()

        self.new_doc_nombre = ""
        self.new_doc_correo = ""
        self.new_doc_pass = ""
        self.error_new_doc = ""
        self.cargar_docentes()
        self.cargar_estadisticas_admin()

    def cargar_estudiantes(self):
        if self.usuario_rol != "admin":
            return rx.redirect("/dashboard")
        with rx.session() as session:
            statement = sqlmodel.select(Usuario).join(Estudiante).where(Usuario.id_usuario == Estudiante.usuario_id)
            resultados = session.exec(statement).all()
            self.lista_estudiantes = [{"id": str(u.id_usuario), "nombre": u.nombreUsuario, "correo": u.correo, "estado": "Activo" if u.activo else "Inactivo"} for u in resultados]

    def toggle_estado_estudiante(self, id_usuario_str: str):
        with rx.session() as session:
            usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.id_usuario == int(id_usuario_str))).first()
            if usuario:
                from datetime import datetime
                usuario.activo = not usuario.activo
                usuario.fecha_desactivacion = datetime.utcnow() if not usuario.activo else None
                session.add(usuario)
                session.commit()
        self.cargar_estudiantes()
        self.cargar_estadisticas_admin()

    lista_usuarios_reset: list[dict[str, str]] = []
    busqueda_reset: str = ""
    reset_usuario_id: str = ""
    reset_usuario_nombre: str = ""
    reset_nueva_pass: str = ""
    modal_reset_abierto: bool = False

    def set_busqueda_reset(self, valor: str):
        self.busqueda_reset = valor

    def set_reset_nueva_pass(self, valor: str):
        self.reset_nueva_pass = valor

    def cargar_usuarios_reset(self):
        if self.usuario_rol != "admin":
            return rx.redirect("/dashboard")
        with rx.session() as session:
            usuarios = session.exec(
                sqlmodel.select(Usuario).where(Usuario.activo == True)
            ).all()
            self.lista_usuarios_reset = [
                {"id": str(u.id_usuario), "nombre": u.nombreUsuario, "correo": u.correo, "rol": u.rol.capitalize()}
                for u in usuarios if u.rol != "admin"
            ]

    @rx.var
    def usuarios_reset_filtrados(self) -> list[dict[str, str]]:
        if not self.busqueda_reset:
            return self.lista_usuarios_reset
        busq = self.busqueda_reset.lower()
        return [u for u in self.lista_usuarios_reset if busq in u["nombre"].lower() or busq in u["correo"].lower()]

    def abrir_modal_reset(self, id_usuario: str, nombre: str):
        self.reset_usuario_id = id_usuario
        self.reset_usuario_nombre = nombre
        self.reset_nueva_pass = ""
        self.modal_reset_abierto = True

    def cerrar_modal_reset(self, _valor: bool = False):
        self.modal_reset_abierto = False
        self.reset_usuario_id = ""
        self.reset_usuario_nombre = ""
        self.reset_nueva_pass = ""

    def confirmar_reset_password(self):
        if not self.reset_nueva_pass.strip():
            return rx.toast.error("Debes escribir una nueva contraseña.", position="bottom-right")

        if len(self.reset_nueva_pass.strip()) < 6:
            return rx.toast.error("La contraseña debe tener al menos 6 caracteres.", position="bottom-right")

        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.id_usuario == int(self.reset_usuario_id))
            ).first()
            if not usuario:
                return rx.toast.error("Usuario no encontrado.", position="bottom-right")

            usuario.contraseñaHash = self._hash_password(self.reset_nueva_pass.strip())
            usuario.debe_cambiar_pass = True
            session.add(usuario)
            session.commit()

        nombre = self.reset_usuario_nombre
        self.cerrar_modal_reset()
        return rx.toast.success(f"Contraseña de '{nombre}' reseteada correctamente. Deberá cambiarla al iniciar sesión.", position="bottom-right")
