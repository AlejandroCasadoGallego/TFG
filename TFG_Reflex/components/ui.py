import reflex as rx
from ..State import State

# =======================================================
# COMPONENTES ATÓMICOS (ESTILOS FIJOS)
# =======================================================

def stat_card(titulo: str, valor: str, icono: str, color_bg: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.center(
                rx.icon(icono, size=28, color="white"),
                background_color=color_bg,
                border_radius="12px",
                width="60px",
                height="60px",
                box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
            ),
            rx.vstack(
                rx.text(titulo, size="2", weight="bold", color="#4b5563"),
                rx.text(valor, size="7", weight="bold", color="#111827"),
                spacing="1",
                align_items="start"
            ),
            align="center",
            spacing="4"
        ),
        size="3",
        width="100%",
        background_color="white",
        border="1px solid #e5e7eb"
    )

def sidebar_item(texto: str, icon: str, ruta: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color="#4b5563"),
            rx.text(texto, size="3", weight="medium", color="#374151"),
            spacing="3",
            padding="12px 16px",
            border_radius="8px",
            _hover={
                "background_color": "#e0e7ff",
                "color": "#4338ca",
            },
            width="100%",
            align="center"
        ),
        href=ruta,
        underline="none",
        width="100%"
    )

# =======================================================
# MENÚS ESPECÍFICOS POR ROL
# =======================================================

def menu_estudiante():
    return rx.vstack(
        rx.text("GESTIÓN ACADÉMICA", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Mis Asignaturas", "book-marked", "#"),
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
        sidebar_item("Gestión Estudiantes", "users", "#"),
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
        sidebar_item("Gestión Usuarios", "users-round", "#"),
        sidebar_item("Resetear Contraseñas", "key-round", "#"),
        
        rx.text("SISTEMA", size="1", weight="bold", color="#9ca3af", margin_top="1em", padding_left="1em"),
        sidebar_item("Gestión de Patrones", "layout-template", "#"),
        sidebar_item("Asignar Docentes", "user-plus", "#"),
        sidebar_item("Configuración General", "settings-2", "#"),
        sidebar_item("Control Accesos", "shield-check", "#"),
        width="100%",
        spacing="1"
    )

# =======================================================
# COMPONENTES DE ESTRUCTURA
# =======================================================

def header_component() -> rx.Component:
    return rx.hstack(
        rx.heading("Panel de Control", size="6", weight="bold", color="#111827"),
        rx.spacer(),
        rx.hstack(
            rx.avatar(fallback=State.usuario_actual[:2], size="4", radius="full", color_scheme="indigo"),
            rx.vstack(
                rx.text(State.usuario_actual, weight="bold", size="3", color="#111827"),
                rx.text(State.usuario_rol.capitalize(), color="#6b7280", size="2"),
                spacing="0",
                align_items="end"
            ),
            spacing="3",
            align="center",
            background_color="white",
            padding="0.5em 1em",
            border_radius="full",
            border="1px solid #e5e7eb"
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

                sidebar_item("Biblioteca de Patrones", "layout-template", "/dashboard"),
                
                rx.match(
                    State.usuario_rol,
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
                on_click=State.cerrar_sesion,
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

# =======================================================
# VISTAS ESPECÍFICAS POR ROL (TEMPORALES)
# =======================================================

def vista_admin() -> rx.Component:
    return rx.vstack(
        rx.grid(
            stat_card("Total Usuarios", "150", "users", "#4f46e5"),
            stat_card("Docentes", "20", "graduation-cap", "#0891b2"),
            stat_card("Estudiantes", "130", "user-plus", "#16a34a"),
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

# =======================================================
# PÁGINAS PRINCIPALES
# =======================================================

def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.icon("graduation-cap", size=48, color="white"),
                    background_color="#4f46e5",
                    padding="1.5em",
                    border_radius="50%",
                    margin_bottom="1em",
                    box_shadow="lg"
                ),
                rx.heading("Acceso", size="7", weight="bold", color="#111827"),
                rx.text("Plataforma de Patrones de Diseño", color="#6b7280", margin_bottom="2em"),
                rx.vstack(
                    rx.text("Correo Electrónico", size="2", weight="bold", color="#374151", width="100%"),
                    rx.input(placeholder="admin@test.com", on_change=State.set_correo_input, size="3", width="100%", variant="soft", color="#000000", background_color="#f3f4f6"),
                    spacing="2", width="100%"
                ),
                rx.vstack(
                    rx.text("Contraseña", size="2", weight="bold", color="#374151", width="100%"),
                    rx.input(type="password", placeholder="••••••••", on_change=State.set_pass_input, size="3", width="100%", variant="soft", color="#000000", background_color="#f3f4f6"),
                    spacing="2", width="100%", margin_top="1em"
                ),
                rx.cond(
                    State.error_mensaje != "",
                    rx.callout(State.error_mensaje, icon="triangle-alert", color_scheme="red", variant="surface", width="100%", margin_top="1em"),
                ),
                rx.button("Entrar", on_click=State.iniciar_sesion, size="4", width="100%", margin_top="2em", cursor="pointer", background_color="#4f46e5", color="white"),
                rx.button("Generar Usuario Demo", on_click=State.crear_usuario_prueba, variant="ghost", color="#6b7280", margin_top="1em", size="2"),
                padding="2em", align="center", width="100%"
            ),
            size="4", max_width="400px", background_color="white", border="1px solid #e5e7eb", box_shadow="xl"
        ),
        height="100vh", background_color="#f3f4f6"
    )

def index_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(),
                rx.match(
                    State.usuario_rol,
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
            flex="1",
            height="100vh",
            background_color="#f9fafb",
            overflow="auto"
        ),
        width="100%"
    )