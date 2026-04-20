import reflex as rx
import sqlmodel
from typing import List
from .base_state import BaseState
from ..models.usuarios import Grupos, Usuario

class GrupoState(BaseState):
    nuevo_nombre: str = ""
    error_creacion: str = ""
    mis_grupos: List[Grupos] = []
    
    destinatarios_input: str = ""
    modal_envio_abierto: bool = False
    grupo_sel_nombre: str = ""
    grupo_sel_codigo: str = ""
    busqueda_estudiante: str = ""
    todos_los_estudiantes: List[str] = []
    estudiantes_seleccionados: List[str] = []

    modal_editar_abierto: bool = False
    grupo_editar_id: int = -1
    grupo_editar_nombre: str = ""
    grupo_editar_codigo: str = ""
    
    miembros_actuales: list[dict[str, str]] = []
    busqueda_invitar: str = ""
    candidatos_invitacion: list[str] = []
    seleccionados_invitar: list[str] = []

    total_mis_grupos: int = 0

    def cargar_grupos(self):
        with rx.session() as session:
            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            
            if profesor:
                self.mis_grupos = session.exec(
                    sqlmodel.select(Grupos).where(Grupos.docente_id == profesor.id_usuario)
                ).all()

    def limpiar_formulario(self):
        self.nuevo_nombre = ""
        self.error_creacion = ""

    def crear_grupo(self):
        self.error_creacion = ""
        if not self.nuevo_nombre.strip():
            self.error_creacion = "El nombre del grupo no puede estar vacío."
            return 

        with rx.session() as session:
            try:
                profesor = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
                if not profesor:
                    self.error_creacion = "Error de sesión: No se ha podido identificar al usuario."
                    return

                existente = session.exec(
                    sqlmodel.select(Grupos).where(
                        (Grupos.nombre == self.nuevo_nombre.strip()) & 
                        (Grupos.docente_id == profesor.id_usuario)
                    )
                ).first()

                if existente:
                    self.error_creacion = "Ya tienes un grupo con este nombre. Elige otro."
                    return

                nuevo_grupo = Grupos(
                    nombre=self.nuevo_nombre.strip(),
                    codigo_acceso=Grupos.generar_codigo(), 
                    docente_id=profesor.id_usuario 
                )
                
                session.add(nuevo_grupo)
                session.commit()
                session.refresh(nuevo_grupo)
                
                codigo_generado = nuevo_grupo.codigo_acceso
                
                self.cargar_grupos()
                self.limpiar_formulario()
                
                return rx.toast.success("¡Grupo creado con éxito!", description=f"El código para los alumnos es: {codigo_generado}", position="bottom-right", duration=10000, close_button=True)

            except Exception as e:
                print(f"Error al crear grupo: {e}")
                self.error_creacion = "Hubo un error al crear el grupo. Inténtalo de nuevo."
                return 

    def abrir_modal_envio(self, id_grupo: int, nombre: str, codigo: str):
        self.grupo_sel_nombre = nombre
        self.grupo_sel_codigo = codigo
        self.modal_envio_abierto = True
        self.busqueda_estudiante = ""
        self.estudiantes_seleccionados = []
        
        with rx.session() as session:
            from ..models.usuarios import Usuario, EstudianteGrupo
            
            estudiantes_sistema = session.exec(
                sqlmodel.select(Usuario).where(Usuario.rol == "estudiante")
            ).all()
            self.todos_los_estudiantes = [e.nombreUsuario for e in estudiantes_sistema]

            miembros_actuales = session.exec(
                sqlmodel.select(Usuario.nombreUsuario)
                .join(EstudianteGrupo, Usuario.id_usuario == EstudianteGrupo.estudiante_id)
                .where(EstudianteGrupo.grupo_id == id_grupo)
            ).all()

            self.estudiantes_seleccionados = list(miembros_actuales)

    def cambiar_estado_modal(self, valor: bool):
        self.modal_envio_abierto = valor
        if not valor:
            self.destinatarios_input = ""

    def enviar_codigo(self):
        if not self.estudiantes_seleccionados:
            return rx.toast.error("Selecciona al menos un estudiante de la lista.", position="bottom-right")
            
        with rx.session() as session:
            remitente = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
            enviados = 0
            from ..models.usuarios import Notificacion
            
            for nombre in self.estudiantes_seleccionados:
                destinatario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == nombre)).first()
                if destinatario:
                    nueva_notif = Notificacion(
                        remitente_id=remitente.id_usuario,
                        destinatario_id=destinatario.id_usuario,
                        titulo=f"Invitación al grupo: {self.grupo_sel_nombre}",
                        mensaje=f"Tu profesor te ha invitado a unirte a el grupo.\n\nTu código de acceso es: {self.grupo_sel_codigo}\n\nCópialo y úsalo en la sección 'Grupos'.",
                        leida=False
                    )
                    session.add(nueva_notif)
                    enviados += 1
                    
            session.commit()
            
            self.cambiar_estado_modal(False)
            return rx.toast.success(f"¡Invitación enviada a {enviados} alumnos!", position="bottom-right")
            
    @rx.var
    def estudiantes_filtrados(self) -> List[str]:
        if not self.busqueda_estudiante:
            return self.todos_los_estudiantes
        busqueda = self.busqueda_estudiante.lower()
        return [e for e in self.todos_los_estudiantes if busqueda in e.lower()]
    
    def toggle_estudiante(self, nombre: str):
        if nombre in self.estudiantes_seleccionados:
            self.estudiantes_seleccionados.remove(nombre)
        else:
            self.estudiantes_seleccionados.append(nombre)

    def cambiar_estado_modal(self, valor: bool):
        self.modal_envio_abierto = valor
        if not valor:
            self.busqueda_estudiante = ""
            self.estudiantes_seleccionados = []

    def eliminar_grupo(self, id_grupo: int):
        with rx.session() as session:
            from ..models.usuarios import Grupos, EstudianteGrupo
            
            matriculas = session.exec(sqlmodel.select(EstudianteGrupo).where(EstudianteGrupo.grupo_id == id_grupo)).all()
            for m in matriculas:
                session.delete(m)
                
            grupo = session.exec(sqlmodel.select(Grupos).where(Grupos.id_grupo == id_grupo)).first()
            if grupo:
                session.delete(grupo)
                session.commit()
                self.cargar_grupos()
                return rx.toast.success("Grupo eliminado correctamente.", position="bottom-right")

    def abrir_modal_editar(self, id_grupo: int, nombre: str, codigo: str):
        self.grupo_editar_id = id_grupo
        self.grupo_editar_nombre = nombre
        self.grupo_editar_codigo = codigo
        self.modal_editar_abierto = True
        self.busqueda_invitar = ""
        self.seleccionados_invitar = []
        self.cargar_datos_edicion()

    def cargar_datos_edicion(self):
        with rx.session() as session:
            from ..models.usuarios import Usuario, EstudianteGrupo
            
            miembros = session.exec(
                sqlmodel.select(Usuario.id_usuario, Usuario.nombreUsuario)
                .join(EstudianteGrupo, Usuario.id_usuario == EstudianteGrupo.estudiante_id)
                .where(EstudianteGrupo.grupo_id == self.grupo_editar_id)
            ).all()
            self.miembros_actuales = [
                {
                    "id": str(m[0]),
                    "nombre": str(m[1]),
                    "iniciales": str(m[1])[:2].upper()
                } for m in miembros
            ]

            ids_miembros = [m[0] for m in miembros]
            if ids_miembros:
                candidatos = session.exec(
                    sqlmodel.select(Usuario.nombreUsuario)
                    .where(Usuario.rol == "estudiante")
                    .where(Usuario.id_usuario.notin_(ids_miembros))
                ).all()
            else:
                candidatos = session.exec(sqlmodel.select(Usuario.nombreUsuario).where(Usuario.rol == "estudiante")).all()
                
            self.candidatos_invitacion = list(candidatos)

    @rx.var
    def candidatos_filtrados(self) -> list[str]:
        
        if not self.busqueda_invitar:
            return self.candidatos_invitacion
        busqueda = self.busqueda_invitar.lower()
        return [c for c in self.candidatos_invitacion if busqueda in c.lower()]

    def toggle_invitar(self, nombre: str):
        if nombre in self.seleccionados_invitar:
            self.seleccionados_invitar.remove(nombre)
        else:
            self.seleccionados_invitar.append(nombre)

    def cambiar_estado_editar(self, valor: bool):
        self.modal_editar_abierto = valor

    def guardar_edicion(self):
        if not self.grupo_editar_nombre.strip():
            return rx.toast.error("El nombre del grupo no puede estar vacío.", position="bottom-right")

        with rx.session() as session:
            from ..models.usuarios import Grupos, Usuario, Notificacion
            
            grupo = session.exec(sqlmodel.select(Grupos).where(Grupos.id_grupo == self.grupo_editar_id)).first()
            if grupo and grupo.nombre != self.grupo_editar_nombre:
                grupo.nombre = self.grupo_editar_nombre.strip()
                session.add(grupo)

            if self.seleccionados_invitar:
                remitente = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
                for nombre in self.seleccionados_invitar:
                    destinatario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == nombre)).first()
                    if destinatario:
                        nueva_notif = Notificacion(
                            remitente_id=remitente.id_usuario,
                            destinatario_id=destinatario.id_usuario,
                            titulo=f"Invitación al grupo: {self.grupo_editar_nombre}",
                            mensaje=f"El profesor te ha invitado a unirte a la clase.\n\nCódigo de acceso: {self.grupo_editar_codigo}",
                            leida=False
                        )
                        session.add(nueva_notif)

            session.commit()

        self.modal_editar_abierto = False
        self.cargar_grupos()
        if self.seleccionados_invitar:
            return rx.toast.success(f"Grupo actualizado e invitaciones enviadas a {len(self.seleccionados_invitar)} alumnos.", position="bottom-right")
        return rx.toast.success("Grupo actualizado correctamente.", position="bottom-right")

    def expulsar_miembro(self, id_estudiante: int, nombre_estudiante: str):
        with rx.session() as session:
            from ..models.usuarios import EstudianteGrupo, Usuario, Notificacion
            
            matricula = session.exec(
                sqlmodel.select(EstudianteGrupo)
                .where((EstudianteGrupo.grupo_id == self.grupo_editar_id) & (EstudianteGrupo.estudiante_id == id_estudiante))
            ).first()
            
            if matricula:
                session.delete(matricula)

                remitente = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
                nueva_notif = Notificacion(
                    remitente_id=remitente.id_usuario,
                    destinatario_id=id_estudiante,
                    titulo=f"Aviso sobre el grupo: {self.grupo_editar_nombre}",
                    mensaje=f"Has sido desvinculado del grupo '{self.grupo_editar_nombre}'. Ya no tienes acceso a este grupo.",
                    leida=False
                )
                session.add(nueva_notif)
                session.commit()

        self.cargar_datos_edicion()
        return rx.toast.info(f"{nombre_estudiante} ha sido expulsado del grupo.", position="bottom-right")
    
    def contar_mis_grupos(self):
        
        if not self.usuario_actual:
            return
            
        with rx.session() as session:
            from ..models.usuarios import Grupos, Usuario
            
            profesor = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            
            if profesor:
                grupos = session.exec(
                    sqlmodel.select(Grupos).where(Grupos.docente_id == profesor.id_usuario)
                ).all()
                
                self.total_mis_grupos = len(grupos)