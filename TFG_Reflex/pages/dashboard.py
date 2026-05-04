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

def render_alumno_dashboard(alumno: dict) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=alumno["iniciales"], size="2", radius="full", color_scheme="indigo"),
        rx.vstack(
            rx.text(alumno["nombre"], weight="bold", size="2", color="#111827"),
            rx.text(alumno["grupo"], size="1", color="#6b7280"),
            spacing="0"
        ),
        rx.spacer(),
        rx.button(
            rx.icon("file-text", size=14), "Ver Informe",
            size="1", variant="soft", color_scheme="blue", cursor="pointer",
            on_click=rx.redirect(f"/informe-estudiante/{alumno['id']}")
        ),
        width="100%", padding="0.75em", border_bottom="1px solid #f3f4f6", align="center"
    )

def vista_docente() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Mis Grupos", valor=GrupoState.total_mis_grupos.to_string(), icono="users", color_bg="#4f46e5", ruta="/mis-grupos"),
            stat_card("Tareas para Corregir", valor=DashboardState.tareas_para_corregir, icono="clock", color_bg="#d97706"),
            stat_card("Tareas Activas", valor=DashboardState.tareas_activas, icono="book-open", color_bg="#0891b2"),
            columns="3", spacing="5", width="100%"
        ),
        
        rx.card(
            rx.vstack(
                rx.text("Mis Alumnos", weight="bold", size="4", color="#111827"),
                rx.text("Acceso rápido a los informes de tus estudiantes.", color="#6b7280", size="2"),
                rx.divider(margin_y="1em"),
                
                rx.cond(
                    DashboardState.alumnos_docente.length() > 0,
                    rx.box(
                        rx.vstack(
                            rx.foreach(DashboardState.alumnos_docente, render_alumno_dashboard),
                            width="100%", spacing="0"
                        ),
                        max_height="300px", overflow="auto"
                    ),
                    rx.center(
                        rx.text("No tienes alumnos en tus grupos.", color="#6b7280", font_style="italic"),
                        padding="2em"
                    )
                ),
                width="100%", align_items="start"
            ),
            width="100%", margin_top="2em", box_shadow="sm", border="1px solid #e5e7eb", background_color="white"
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