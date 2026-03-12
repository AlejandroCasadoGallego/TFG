import reflex as rx
from ..state.base_state import BaseState
from ..state.admin_state import AdminState
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
            stat_card("Mis Grupos", "4", "users", "#4f46e5"),
            stat_card("Tareas para Corregir", "12", "clock", "#d97706"),
            stat_card("Tareas Activas", "5", "book-open", "#0891b2"),
            columns="3", spacing="5", width="100%"
        ),
        width="100%"
    )

def vista_estudiante() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Tareas Pendientes", "3", "clipboard-list", "#d97706"),
            stat_card("Tareas Completadas", "8", "circle-check", "#16a34a"),
            stat_card("Mi Media", "8.2", "star", "#eab308"),
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