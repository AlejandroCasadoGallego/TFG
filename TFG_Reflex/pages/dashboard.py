import reflex as rx
from ..state.base_state import BaseState
from ..state.admin_state import AdminState
from ..state.grupo_state import GrupoState
from ..state.dashboard_state import DashboardState
from ..components.layout import sidebar_layout, header_component
from ..components.ui_elements import stat_card

def vista_admin() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Total Usuarios", "150", "users", "#4f46e5"),
            stat_card("Docentes", valor=AdminState.total_docentes, icono="graduation-cap", color_bg="#0891b2", ruta="/gestion-docentes"),
            stat_card("Estudiantes", valor=AdminState.total_estudiantes, icono="user-plus", color_bg="#16a34a", ruta="/gestion-estudiantes"),
            stat_card("Alertas Sistema", "0", "shield-check", "#ef4444"),
            columns="4", spacing="5", width="100%"
        ),
        width="100%"
    )

def vista_docente() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Mis Grupos", valor=GrupoState.total_mis_grupos.to_string(), icono="users", color_bg="#4f46e5", ruta="/mis-grupos"),
            stat_card("Tareas para Corregir", valor=DashboardState.tareas_para_corregir, icono="clock", color_bg="#d97706"),
            stat_card("Tareas Activas", valor=DashboardState.tareas_activas, icono="book-open", color_bg="#0891b2"),
            columns="3", spacing="5", width="100%"
        ),
        width="100%"
    )

def vista_estudiante() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Tareas Pendientes", valor=DashboardState.tareas_pendientes, icono="clipboard-list", color_bg="#d97706", ruta="/mis-tareas-estudiante"),
            stat_card("Tareas Completadas", valor=DashboardState.tareas_completadas, icono="circle-check", color_bg="#16a34a", ruta="/mis-tareas-estudiante"),
            stat_card("Mi Media", valor=DashboardState.mi_media, icono="star", color_bg="#eab308"),
            columns="3", spacing="5", width="100%"
        ),
        width="100%"
    )

def index_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(),
                rx.match(
                    BaseState.usuario_rol,
                    ("admin", vista_admin()),
                    ("docente", vista_docente()),
                    ("estudiante", vista_estudiante()),
                    vista_estudiante(),
                ),
                padding="3em",
                max_width="1400px",
                margin="0 auto",
                width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )