import reflex as rx
from .state.base_state import BaseState
from .state.auth_state import AuthState
from .state.profile_state import ProfileState
from .state.admin_state import AdminState
from .pages.public import landing_page, login_page, register_page, primer_acceso_page
from .pages.dashboard import index_page
from .pages.profile import perfil_page, editar_perfil_page
from .pages.admin_management import gestion_docentes_page, gestion_estudiantes_page
from .state.patterns_state import PatternsState
from .pages.patterns_library import biblioteca_page
from .pages.create_pattern import create_pattern_page
from .state.pattern_detail_state import PatternDetailState
from .pages.pattern_detail import pattern_detail_page
from .state.edit_pattern_state import EditPatternState
from .pages.edit_pattern import edit_pattern_page
from .pages.docente_grupos import docente_grupos_page
from .state.grupo_state import GrupoState
from .pages.estudiante_grupos import estudiante_grupos_page
from .state.estudiante_grupos_state import EstudianteGruposState
from .pages.estudiante_tareas import estudiante_tareas_page
from .state.estudiante_tareas_state import EstudianteTareasState
from .pages.notificaciones import notificaciones_page
from .pages.crear_tarea import crear_tarea_page
from .state.tarea_state import TareaState
from .pages.mis_tareas import mis_tareas_page
from .state.mis_tareas_state import MisTareasState
from .pages.tarea_detail import tarea_detail_page
from .pages.editar_tarea import editar_tarea_page
from .pages.resolver_tarea import resolver_tarea_page
from .state.resolver_tarea_state import ResolverTareaState
from .pages.evaluar_tarea import evaluar_tarea_page
from .state.evaluar_tarea_state import EvaluarTareaState
from .state.dashboard_state import DashboardState
from .pages.mensajes_alumnos import mensajes_alumnos_page
from .state.mensajes_state import MensajesState
from .models import *

app = rx.App(
    theme=rx.theme(appearance="light", has_background=True, radius="large", accent_color="indigo"))

app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(index_page, route="/dashboard", on_load=[BaseState.check_login, AdminState.cargar_estadisticas_admin, GrupoState.contar_mis_grupos, DashboardState.cargar_estadisticas_dashboard])
app.add_page(perfil_page, route="/perfil", on_load=ProfileState.cargar_perfil)
app.add_page(editar_perfil_page, route="/editar-perfil", on_load=BaseState.check_login)
app.add_page(gestion_docentes_page, route="/gestion-docentes", on_load=AdminState.cargar_docentes)
app.add_page(primer_acceso_page, route="/primer-acceso", on_load=BaseState.check_login)
app.add_page(gestion_estudiantes_page, route="/gestion-estudiantes", on_load=AdminState.cargar_estudiantes)
app.add_page(biblioteca_page, route="/biblioteca", on_load=PatternsState.cargar_patrones)
app.add_page(create_pattern_page, route="/crear-patron", on_load=BaseState.check_login)
app.add_page(pattern_detail_page, route="/patron/[id_patron]", on_load=PatternDetailState.cargar_patron)
app.add_page(edit_pattern_page, route="/editar-patron/[id_patron]", on_load=EditPatternState.cargar_datos)
app.add_page(docente_grupos_page, route="/mis-grupos", on_load=[BaseState.check_login, GrupoState.cargar_grupos])
app.add_page(estudiante_grupos_page, route="/mis-grupos-estudiante", on_load=[BaseState.check_login, EstudianteGruposState.cargar_grupos])
app.add_page(estudiante_tareas_page, route="/mis-tareas-estudiante", on_load=[BaseState.check_login, EstudianteTareasState.cargar_tareas])
app.add_page(notificaciones_page, route="/notificaciones", on_load=[BaseState.check_login, BaseState.cargar_notificaciones])
app.add_page(crear_tarea_page, route="/crear-tarea", on_load=[BaseState.check_login, TareaState.cargar_datos_formulario])
app.add_page(mis_tareas_page, route="/mis-tareas", on_load=[BaseState.check_login, MisTareasState.cargar_tareas])
app.add_page(tarea_detail_page, route="/tarea/[id_tarea]", on_load=[BaseState.check_login, MisTareasState.cargar_detalle_tarea])
app.add_page(editar_tarea_page, route="/editar-tarea/[id_tarea]", on_load=[BaseState.check_login, TareaState.cargar_tarea_edicion])
app.add_page(resolver_tarea_page, route="/resolver-tarea/[id_tarea]", on_load=[BaseState.check_login, ResolverTareaState.cargar_tarea])
app.add_page(mensajes_alumnos_page, route="/mensajes-alumnos", on_load=[BaseState.check_login, MensajesState.cargar_mensajes])
