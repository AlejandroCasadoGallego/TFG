import reflex as rx
from ..state.base_state import BaseState
from .ui_elements import sidebar_item
from ..colores import *

def menu_estudiante():
    return rx.vstack(
        rx.text("GESTIÓN ACADÉMICA", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Grupos", "users", "/mis-grupos-estudiante"),
        sidebar_item("Mis Tareas", "clipboard-list", "/mis-tareas-estudiante"),
        sidebar_item("Mi Resumen", "bar-chart-3", "/mi-resumen"),
        
        rx.text("COMUNICACIÓN", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Notificaciones", "bell", "/notificaciones"),
        width="100%",
        spacing="1"
    )

def menu_docente():
    return rx.vstack(
        rx.text("CONTENIDO", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Crear Tarea", "circle-plus", "/crear-tarea"),
        sidebar_item("Mis Tareas", "list-checks", "/mis-tareas"), 
        
        rx.text("SEGUIMIENTO", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Mis Grupos", "users", "/mis-grupos"),
        
        rx.text("COMUNICACIÓN", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Mensajes Alumnos", "message-square", "/mensajes-alumnos"),
        width="100%",
        spacing="1"
    )

def menu_administrador():
    return rx.vstack(
        rx.text("USUARIOS", size="1", weight="bold", color=color_texto_claro, margin_top="1em", padding_left="1em"),
        sidebar_item("Gestión Docentes", "graduation-cap", "/gestion-docentes"),
        sidebar_item("Gestión Estudiantes", "users", "/gestion-estudiantes"),
        sidebar_item("Resetear Contraseñas", "key-round", "/resetear-contrasenas"),
        width="100%",
        spacing="1"
    )

def header_component(titulo: str = "Panel de Control")-> rx.Component:
    return rx.hstack(
        rx.heading(titulo, size="6", weight="bold", color=color_texto_principal),
        rx.spacer(),
        rx.link(
            rx.box(
                rx.icon("bell", size=24, color=color_texto_gris),
                rx.cond(
                    BaseState.notificaciones_sin_leer > 0,
                    rx.box(
                        rx.text(BaseState.notificaciones_sin_leer, size="1", weight="bold", color="white"),
                        position="absolute",
                        top="-5px",
                        right="-5px",
                        background_color=color_error,
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
                    rx.text(BaseState.usuario_actual, weight="bold", size="3", color=color_texto_principal),
                    rx.text(BaseState.usuario_rol.capitalize(), color=color_texto_gris, size="2"),
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
            rx.icon("library", color=color_primario, size=32),
            rx.heading("PatternLab", size="5", weight="bold", color=color_texto_principal),
            align="center",
            spacing="3",
            padding="2em",
        ),
        rx.divider(background_color=color_borde),
        
        rx.scroll_area(
            rx.vstack(
                sidebar_item("Inicio", "home", "/dashboard"),
                sidebar_item("Biblioteca de Patrones", "layout-template", "/biblioteca"),
                sidebar_item("Leyenda Diagramas", "book-open", "/leyenda-diagramas"),
                
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
                background_color=color_error_fondo,
                color=color_error_intenso,
                width="100%"
            ),
            padding="2em",
            width="100%"
        ),
        width="280px",
        height="100vh",
        background_color="white",
        border_right=f"1px solid {color_borde}",
        display=["none", "none", "flex", "flex"]
    )

def public_header() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.hstack(
                rx.icon("library", color=color_primario, size=28),
                rx.heading("PatternLab", size="5", weight="bold", color=color_texto_principal),
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
        width="100%", padding="1em 2em", background_color="white", border_bottom=f"1px solid {color_borde}", align="center"
    )