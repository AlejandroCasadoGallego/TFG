import reflex as rx
from ..state.mis_tareas_state import MisTareasState, PreguntaDetalleUI, EstudianteAsignadoUI
from ..components.layout import sidebar_layout, header_component
from .mis_tareas import modal_confirmar_eliminacion


def resumen_item(icono: str, etiqueta: str, valor: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icono, size=18, color="#4f46e5"),
            rx.vstack(
                rx.text(etiqueta, size="1", color="#6b7280", weight="bold"),
                rx.text(valor, size="2", color="#111827", weight="medium"),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        padding="1em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        width="100%",
    )


def render_opcion(opcion: str) -> rx.Component:
    return rx.hstack(
        rx.icon("circle", size=10, color="#6366f1"),
        rx.text(opcion, size="2", color="#374151"),
        spacing="2",
        align="center",
        width="100%",
        padding="0.5em 0",
    )


def render_pregunta_detalle(pregunta: PreguntaDetalleUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(f"Pregunta {pregunta.numero}", color_scheme="indigo", variant="soft"),
                rx.badge(pregunta.tipo, color_scheme="gray", variant="surface"),
                width="100%",
                align="center",
                spacing="2",
            ),
            rx.text(pregunta.enunciado, color="#111827", size="3", white_space="pre-wrap", line_height="1.6"),
            rx.cond(
                pregunta.opciones.length() > 0,
                rx.vstack(
                    rx.text("Opciones", size="2", color="#374151", weight="bold"),
                    rx.vstack(
                        rx.foreach(pregunta.opciones, render_opcion),
                        width="100%",
                        spacing="0",
                    ),
                    width="100%",
                    align_items="start",
                    margin_top="0.5em",
                ),
            ),
            rx.cond(
                pregunta.respuesta_correcta != "",
                rx.box(
                    rx.hstack(
                        rx.icon("check", size=16, color="#16a34a"),
                        rx.text("Respuesta correcta:", size="2", color="#166534", weight="bold"),
                        rx.text(pregunta.respuesta_correcta, size="2", color="#166534"),
                        spacing="2",
                        align="center",
                    ),
                    padding="0.75em",
                    background_color="#f0fdf4",
                    border="1px solid #bbf7d0",
                    border_radius="8px",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        width="100%",
        padding="1.25em",
        background_color="white",
        border="1px solid #e5e7eb",
        box_shadow="sm",
    )


def color_estado(estado: str) -> str:
    return rx.match(
        estado,
        ("Pendiente", "yellow"),
        ("Entregada", "green"),
        ("Completada", "green"),
        ("Revisada", "blue"),
        "gray",
    )


def render_estudiante_asignado(estudiante: EstudianteAsignadoUI) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=estudiante.nombre[:2].upper(), size="2", radius="full", color_scheme="indigo"),
        rx.vstack(
            rx.text(estudiante.nombre, size="2", color="#111827", weight="bold"),
            rx.text(estudiante.correo, size="1", color="#6b7280"),
            spacing="0",
            align_items="start",
        ),
        rx.spacer(),
        rx.badge(estudiante.estado, color_scheme=color_estado(estudiante.estado), variant="soft"),
        rx.cond(
            estudiante.ha_entregado,
            rx.button(
                "Ver Resolución",
                size="1",
                variant="soft",
                color_scheme="indigo",
                cursor="pointer",
                on_click=rx.redirect(f"/evaluar-resolucion/{MisTareasState.tarea_detalle.id_tarea}/{estudiante.id_estudiante}"),
            ),
        ),
        width="100%",
        padding="0.9em 0",
        border_bottom="1px solid #f3f4f6",
        align="center",
    )


def panel_detalles() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Información de la tarea", size="4", color="#111827"),
            rx.text(MisTareasState.tarea_detalle.descripcion, color="#374151", size="3", white_space="pre-wrap", line_height="1.6"),
            rx.divider(margin_y="0.75em"),
            rx.cond(
                MisTareasState.tarea_detalle.enunciado != "",
                rx.vstack(
                    rx.text("Enunciado", size="2", color="#374151", weight="bold"),
                    rx.text(MisTareasState.tarea_detalle.enunciado, color="#4b5563", size="2", white_space="pre-wrap", line_height="1.6"),
                    align_items="start",
                    width="100%",
                )
            ),
            rx.grid(
                resumen_item("target", "Dificultad", MisTareasState.tarea_detalle.dificultad),
                resumen_item("keyboard", "Tipo de entrada", MisTareasState.tarea_detalle.tipo_entrada),
                resumen_item("rotate-ccw", "Reintentos", MisTareasState.tarea_detalle.permite_reintentos),
                resumen_item("timer", "Tiempo límite", MisTareasState.tarea_detalle.tiempo_limite),
                columns={"initial": "1", "sm": "2"},
                spacing="3",
                width="100%",
                margin_top="1em",
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        padding="1.5em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        border_top_left_radius="0",
    )


def panel_preguntas() -> rx.Component:
    return rx.box(
        rx.cond(
            MisTareasState.preguntas_detalle.length() > 0,
            rx.vstack(
                rx.foreach(MisTareasState.preguntas_detalle, render_pregunta_detalle),
                width="100%",
                spacing="3",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("circle-help", size=40, color="#9ca3af"),
                    rx.text("Esta tarea no tiene preguntas registradas.", color="#6b7280", size="2"),
                    align="center",
                ),
                width="100%",
                padding="3em",
            ),
        ),
        padding="1.5em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        border_top_left_radius="0",
    )


def panel_estudiantes() -> rx.Component:
    return rx.box(
        rx.cond(
            MisTareasState.estudiantes_detalle.length() > 0,
            rx.vstack(
                rx.foreach(MisTareasState.estudiantes_detalle, render_estudiante_asignado),
                width="100%",
                spacing="0",
            ),
            rx.center(
                rx.vstack(
                    rx.icon("users-round", size=40, color="#9ca3af"),
                    rx.text("No hay estudiantes asignados a esta tarea.", color="#6b7280", size="2"),
                    align="center",
                ),
                width="100%",
                padding="3em",
            ),
        ),
        padding="1.5em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        border_top_left_radius="0",
    )


def contenido_detalle_tarea() -> rx.Component:
    return rx.cond(
        MisTareasState.error_detalle,
        rx.center(
            rx.vstack(
                rx.icon("file-warning", size=48, color="#ef4444"),
                rx.heading("Tarea no encontrada", size="6", color="#111827"),
                rx.text("La tarea no existe o no tienes permiso para verla.", color="#6b7280"),
                rx.button("Volver a mis tareas", on_click=rx.redirect("/mis-tareas"), color_scheme="indigo", cursor="pointer"),
                align="center",
                spacing="3",
            ),
            width="100%",
            height="55vh",
        ),
        rx.vstack(
            rx.button(
                rx.icon("arrow-left", size=16),
                "Volver a mis tareas",
                color="#4b5563",
                on_click=rx.redirect("/mis-tareas"),
                variant="ghost",
                color_scheme="gray",
                cursor="pointer",
                margin_bottom="0.5em",
            ),
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading(MisTareasState.tarea_detalle.titulo, size="8", weight="bold", color="#111827"),
                        rx.badge(MisTareasState.tarea_detalle.tipo, color_scheme="indigo", variant="solid"),
                        spacing="3",
                        align="center",
                        flex_wrap="wrap",
                    ),
                    rx.text(MisTareasState.tarea_detalle.grupo, color="#4b5563", size="3", weight="medium"),
                    align_items="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("pencil", size=16),
                    "Modificar",
                    variant="solid",
                    color_scheme="indigo",
                    cursor="pointer",
                    on_click=rx.redirect(f"/editar-tarea/{MisTareasState.tarea_detalle.id_tarea}"),
                ),
                rx.button(
                    rx.icon("trash", size=16),
                    "Eliminar",
                    variant="soft",
                    color_scheme="red",
                    cursor="pointer",
                    on_click=MisTareasState.abrir_modal_eliminar(
                        MisTareasState.tarea_detalle.id_tarea,
                        MisTareasState.tarea_detalle.titulo,
                    ),
                ),
                width="100%",
                align="center",
                flex_wrap="wrap",
                gap="4",
            ),
            rx.grid(
                resumen_item("calendar-days", "Fechas", MisTareasState.tarea_detalle.fechas),
                resumen_item("list-checks", "Preguntas", MisTareasState.tarea_detalle.total_preguntas),
                resumen_item("users", "Estudiantes", MisTareasState.tarea_detalle.total_estudiantes),
                columns={"initial": "1", "sm": "3"},
                spacing="3",
                width="100%",
                margin_y="1.5em",
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("info", size=16, color="#111827"), rx.text("Detalles", weight="bold", color="#111827")),
                        value="detalles",
                        cursor="pointer",
                        color="#111827",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("circle-help", size=16, color="#111827"), rx.text("Preguntas", weight="bold", color="#111827")),
                        value="preguntas",
                        cursor="pointer",
                        color="#111827",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("users", size=16, color="#111827"), rx.text("Estudiantes", weight="bold", color="#111827")),
                        value="estudiantes",
                        cursor="pointer",
                        color="#111827",
                    ),
                    size="2",
                    background_color="white",
                    border="1px solid #e5e7eb",
                    border_bottom="0",
                    border_top_left_radius="8px",
                    border_top_right_radius="8px",
                ),
                rx.tabs.content(panel_detalles(), value="detalles"),
                rx.tabs.content(panel_preguntas(), value="preguntas"),
                rx.tabs.content(panel_estudiantes(), value="estudiantes"),
                default_value="detalles",
                width="100%",
                color_scheme="indigo",
            ),
            width="100%",
            max_width="1100px",
            margin="0 auto",
        ),
    )


def tarea_detail_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Detalle de Tarea"),
                contenido_detalle_tarea(),
                modal_confirmar_eliminacion(),
                width="100%",
                padding="3em",
            ),
            flex="1",
            height="100vh",
            background_color="#f9fafb",
            overflow="auto",
        ),
        width="100%",
    )
