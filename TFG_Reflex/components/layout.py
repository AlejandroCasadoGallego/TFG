import reflex as rx
from ..state.base_state import BaseState
from .ui_elements import sidebar_item

def menu_estudiante():
    return rx.vstack(
        rx.text("GESTIÓN ACADÉMICA", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Grupos", "users", "/mis-grupos-estudiante"),
        sidebar_item("Materiales", "folder-open", "#"),
        sidebar_item("Calendario Entregas", "calendar-clock", "#"),
        
        rx.text("PROGRESO", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Calificaciones", "award", "#"),
        sidebar_item("Histórico Entregas", "history", "#"),
        sidebar_item("Progreso Académico", "trending-up", "#"),
        
        rx.text("COMUNICACIÓN", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Notificaciones", "bell", "#"),
        sidebar_item("Avisos", "megaphone", "#"),
        width="100%",
        spacing="1"
    )

def menu_docente():
    return rx.vstack(
        rx.text("CONTENIDO", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Publicar Materiales", "upload", "#"),
        sidebar_item("Gestión Materiales", "files", "#"),
        sidebar_item("Crear Actividades", "circle-plus", "#"),
        
        rx.text("SEGUIMIENTO", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Mis Grupos", "users", "/mis-grupos"),
        sidebar_item("Ver Entregas", "inbox", "#"),
        sidebar_item("Estadísticas", "bar-chart-3", "#"),
        
        rx.text("COMUNICACIÓN", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Anuncios Clase", "megaphone", "#"),
        sidebar_item("Mensajes Alumnos", "message-square", "#"),
        width="100%",
        spacing="1"
    )

def menu_administrador():
    return rx.vstack(
        rx.text("USUARIOS", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Gestión Docentes", "graduation-cap", "/gestion-docentes"),
        sidebar_item("Gestión Estudiantes", "users", "/gestion-estudiantes"),
        sidebar_item("Resetear Contraseñas", "key-round", "#"),
        
        rx.text("SISTEMA", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Gestión de Patrones", "layout-template", "#"),
        sidebar_item("Asignar Docentes", "user-plus", "#"),
        sidebar_item("Configuración General", "settings-2", "#"),
        sidebar_item("Control Accesos", "shield-check", "#"),
        width="100%",
        spacing="1"
    )

def header_component(titulo: str = "Panel de Control")-> rx.Component:
    return rx.hstack(
        rx.heading(titulo, size="6", weight="bold", color="#111827"),
        rx.spacer(),
        rx.link(
            rx.box(
                rx.icon("bell", size=24, color="#6b7280"),
                rx.cond(
                    BaseState.notificaciones_sin_leer > 0,
                    rx.box(
                        rx.text(BaseState.notificaciones_sin_leer, size="1", weight="bold", color="white"),
                        position="absolute",
                        top="-5px",
                        right="-5px",
                        background_color="#ef4444",
                        border_radius="full",
                        width="18px",
                        height="18px",
                        display="flex",
                        align_items="center",
                        justify_content="center"
                    )
                ),
                position="relative",
                cursor="pointer",
                margin_right="1.5em"
            ),
            href="/notificaciones", 
        ),

        rx.button(
            rx.hstack(
                rx.avatar(fallback=BaseState.usuario_actual[:2], size="4", radius="full", color_scheme="indigo"),
                rx.vstack(
                    rx.text(BaseState.usuario_actual, weight="bold", size="3", color="#111827"),
                    rx.text(BaseState.usuario_rol.capitalize(), color="#6b7280", size="2"),
                    spacing="0",
                    align_items="end"
                ),
                spacing="3",
            ),
            on_click=BaseState.navegar_perfil,
            variant="ghost",
            padding="0.5em 1em",
            border_radius="full",
            cursor="pointer"
        ),
        width="100%",
        margin_bottom="2em",
        align="center"
    )

def sidebar_layout() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("library", color="#4f46e5", size=32),
            rx.heading("PatternLab", size="5", weight="bold", color="#111827"),
            align="center",
            spacing="3",
            padding="2em",
        ),
        rx.divider(background_color="#e5e7eb"),
        
        rx.scroll_area(
            rx.vstack(
                sidebar_item("Inicio", "home", "/dashboard"),
                sidebar_item("Biblioteca de Patrones", "layout-template", "/biblioteca"),
                
                rx.match(
                    BaseState.usuario_rol,
                    ("admin", menu_administrador()),
                    ("docente", menu_docente()),
                    ("estudiante", menu_estudiante()),
                    menu_estudiante(),
                ),
                spacing="2",
                width="100%",
                padding_x="1em",
            ),
            type="hover",
            style={"height": "calc(100vh - 180px)"}
        ),

        rx.spacer(),
        rx.box(
            rx.button(
                rx.hstack(rx.icon("log-out", size=18), rx.text("Cerrar Sesión")),
                on_click=BaseState.cerrar_sesion,
                background_color="#fee2e2",
                color="#991b1b",
                width="100%"
            ),
            padding="2em",
            width="100%"
        ),
        width="280px",
        height="100vh",
        background_color="white",
        border_right="1px solid #e5e7eb",
        display=["none", "none", "flex", "flex"]
    )

def public_header() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.hstack(
                rx.icon("library", color="#4f46e5", size=28),
                rx.heading("PatternLab", size="5", weight="bold", color="#111827"),
                align="center", spacing="3", cursor="pointer"
            ),
            href="/", underline="none"
        ),
        rx.spacer(),
        rx.hstack(
            rx.link(rx.button("Iniciar Sesión", variant="ghost", color_scheme="gray", cursor="pointer"), href="/login"),
            rx.link(rx.button("Regístrate Gratis", color_scheme="indigo", cursor="pointer"), href="/register"),
            spacing="3"
        ),
        width="100%", padding="1em 2em", background_color="white", border_bottom="1px solid #e5e7eb", align="center"
    )