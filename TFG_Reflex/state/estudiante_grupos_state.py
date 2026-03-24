import reflex as rx
import sqlmodel
from typing import List
from .base_state import BaseState
from ..models.usuarios import Grupos, Usuario, Estudiante, EstudianteGrupo

class EstudianteGruposState(BaseState):
    codigo_input: str = ""
    error_union: str = ""
    mis_grupos: List[Grupos] = []

    def cargar_grupos(self):
        with rx.session() as session:
            usuario = session.exec(
                sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)
            ).first()
            
            if usuario:
                statement = sqlmodel.select(Grupos).join(EstudianteGrupo).where(EstudianteGrupo.estudiante_id == usuario.id_usuario)
                self.mis_grupos = session.exec(statement).all()

    def limpiar_formulario(self):
        self.codigo_input = ""
        self.error_union = ""

    def unirse_grupo(self):
        self.error_union = ""
        codigo = self.codigo_input.strip().upper()

        if not codigo:
            self.error_union = "Por favor, introduce el código del grupo."
            return 

        with rx.session() as session:
            try:
                grupo = session.exec(sqlmodel.select(Grupos).where(Grupos.codigo_acceso == codigo)).first()
                if not grupo:
                    self.error_union = "Código no válido. Comprueba si está bien escrito."
                    return 

                usuario = session.exec(sqlmodel.select(Usuario).where(Usuario.nombreUsuario == self.usuario_actual)).first()
                if not usuario:
                    self.error_union = "Error de sesión."
                    return 

                estudiante = session.exec(sqlmodel.select(Estudiante).where(Estudiante.usuario_id == usuario.id_usuario)).first()
                if not estudiante:
                    estudiante = Estudiante(usuario_id=usuario.id_usuario)
                    session.add(estudiante)
                    session.commit()

                ya_unido = session.exec(
                    sqlmodel.select(EstudianteGrupo).where(
                        (EstudianteGrupo.estudiante_id == usuario.id_usuario) & 
                        (EstudianteGrupo.grupo_id == grupo.id_grupo)
                    )
                ).first()

                if ya_unido:
                    self.error_union = "Ya estás matriculado en este grupo."
                    return 

                nueva_matricula = EstudianteGrupo(estudiante_id=usuario.id_usuario, grupo_id=grupo.id_grupo)
                session.add(nueva_matricula)
                session.commit()

                self.cargar_grupos()
                self.limpiar_formulario()
                
                return rx.toast.success(f"¡Te has unido a {grupo.nombre} con éxito!", position="bottom-right")

            except Exception as e:
                print(f"Error al unirse al grupo: {e}")
                self.error_union = "Hubo un error al procesar tu solicitud."
                return