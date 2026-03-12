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
    pass_forzado_1: str = ""
    pass_forzado_2: str = ""
    error_pass_forzado: str = ""

    confirm_delete_input: str = ""
    total_docentes: str = "0"

    datos_perfil: dict = {}

    lista_docentes: list[dict[str, str]] = []
    
    new_doc_nombre: str = ""
    new_doc_correo: str = ""
    new_doc_pass: str = ""
    error_new_doc: str = ""

    total_estudiantes: str = "0"
    lista_estudiantes: list[dict[str, str]] = []

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

    def cerrar_sesion(self):
        """Limpia la sesión y vuelve al login."""
        self.usuario_actual = ""
        return rx.redirect("/")

    def check_login(self):
        """Protección de ruta: si no hay usuario, rebota al login."""
        if not self.usuario_actual:
            return rx.redirect("/")
        if self.usuario_rol == "admin":
            self.cargar_estadisticas_admin()
    
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
        
    def cargar_estadisticas_admin(self):
        """Calcula las estadísticas reales para el dashboard del administrador."""
        with rx.session() as session:
            # Contamos Docentes activos
            docentes = session.exec(
                sqlmodel.select(Docente).join(Usuario).where(Usuario.activo == True)
            ).all()
            self.total_docentes = str(len(docentes))

            # Contamos Estudiantes activos (¡NUEVO!)
            estudiantes = session.exec(
                sqlmodel.select(Estudiante).join(Usuario).where(Usuario.activo == True)
            ).all()
            self.total_estudiantes = str(len(estudiantes))

    def cargar_docentes(self):
        """Carga la lista de docentes para la tabla de gestión."""
        if self.usuario_rol != "admin":
            return rx.redirect("/dashboard")
            
        with rx.session() as session:
            # Hacemos un JOIN para traer los Usuarios que son Docentes
            statement = sqlmodel.select(Usuario).join(Docente).where(Usuario.id_usuario == Docente.usuario_id)
            resultados = session.exec(statement).all()
            
            # Formateamos los datos en una lista de diccionarios para la UI
            self.lista_docentes = [
                {
                    "id": str(u.id_usuario),
                    "nombre": u.nombreUsuario,
                    "correo": u.correo,
                    # Reflex maneja mejor los booleanos si los pasamos como strings explícitos para los estilos
                    "estado": "Activo" if u.activo else "Inactivo" 
                } for u in resultados
            ]

    def toggle_estado_docente(self, id_usuario_str: str):
        """Activa o desactiva a un docente."""
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.id_usuario == int(id_usuario_str))
            ).first()
            
            if usuario:
                usuario.activo = not usuario.activo
                session.add(usuario)
                session.commit()
                
        # Recargamos la lista y las estadísticas
        self.cargar_docentes()
        self.cargar_estadisticas_admin()

    def registrar_docente(self):
        """Crea un nuevo docente desde el panel de admin."""
        with rx.session() as session:
            # Validaciones
            if not self.new_doc_nombre.strip() or not self.new_doc_correo.strip() or not self.new_doc_pass.strip():
                self.error_new_doc = "Todos los campos son obligatorios."
                return
                
            existente = session.exec(sqlmodel.select(Usuario).where(Usuario.correo == self.new_doc_correo.strip())).first()
            if existente:
                self.error_new_doc = "Este correo ya está registrado."
                return

            # Crear Usuario
            nuevo_usuario = Usuario(
                nombreUsuario=self.new_doc_nombre.strip(),
                correo=self.new_doc_correo.strip(),
                contraseñaHash=self._hash_password(self.new_doc_pass.strip()),
                rol="docente",
                activo=True,
                debe_cambiar_pass=True
            )
            session.add(nuevo_usuario)
            session.commit()
            session.refresh(nuevo_usuario)

            # Crear registro en tabla Docente
            session.add(Docente(usuario_id=nuevo_usuario.id_usuario))
            session.commit()

        # Limpiar formulario, cerrar modal y recargar lista
        self.new_doc_nombre = ""
        self.new_doc_correo = ""
        self.new_doc_pass = ""
        self.error_new_doc = ""
        self.cargar_docentes()
        self.cargar_estadisticas_admin()

    def guardar_pass_forzado(self):
        """Valida y guarda la contraseña definitiva del docente."""
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
                    self.error_pass_forzado = "Debes elegir una contraseña diferente a la temporal que te dio el administrador."
                    return
                
                # Actualizamos y liberamos al usuario del cambio forzado
                usuario.contraseñaHash = nuevo_hash
                usuario.debe_cambiar_pass = False
                session.add(usuario)
                session.commit()
                
                # Limpiamos variables y lo dejamos entrar a su dashboard
                self.pass_forzado_1 = ""
                self.pass_forzado_2 = ""
                self.error_pass_forzado = ""
                return rx.redirect("/dashboard")
            
    def cargar_estudiantes(self):
        """Carga la lista de estudiantes para la tabla de gestión."""
        if self.usuario_rol != "admin":
            return rx.redirect("/dashboard")
            
        with rx.session() as session:
            statement = sqlmodel.select(Usuario).join(Estudiante).where(Usuario.id_usuario == Estudiante.usuario_id)
            resultados = session.exec(statement).all()
            
            self.lista_estudiantes = [
                {
                    "id": str(u.id_usuario),
                    "nombre": u.nombreUsuario,
                    "correo": u.correo,
                    "estado": "Activo" if u.activo else "Inactivo"
                } for u in resultados
            ]

    def toggle_estado_estudiante(self, id_usuario_str: str):
        """Activa o desactiva a un estudiante."""
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.id_usuario == int(id_usuario_str))
            ).first()
            
            if usuario:
                usuario.activo = not usuario.activo
                session.add(usuario)
                session.commit()
                
        # Recargamos la lista y el contador del dashboard
        self.cargar_estudiantes()
        self.cargar_estadisticas_admin()