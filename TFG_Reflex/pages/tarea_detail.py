import reflex as rx
from ..state.mis_tareas_state import MisTareasState, PreguntaDetalleUI, EstudianteAsignadoUI
from ..components.layout import sidebar_layout, header_component
from .mis_tareas import modal_confirmar_eliminacion
from ..colores import *


def resumen_item(icono: str, etiqueta: str, valor: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icono, size=18, color=color_primario),
            rx.vstack(
                rx.text(etiqueta, size="1", color=color_texto_gris, weight="bold"),
                rx.text(valor, size="2", color=color_texto_principal, weight="medium"),
                spacing="0",
                align_items="start",
            ),
            spacing="3",
            align="center",
        ),
        padding="1em",
        background_color="white",
        border=f"1px solid {color_borde}",
        border_radius="8px",
        width="100%",
    )


def render_opcion(opcion: str) -> rx.Component:
    return rx.hstack(
        rx.icon("circle", size=10, color=color_indigo_suave),
        rx.text(opcion, size="2", color=color_texto_secundario),
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
            rx.text(pregunta.enunciado, color=color_texto_principal, size="3", white_space="pre-wrap", line_height="1.6"),
            rx.cond(
                pregunta.opciones.length() > 0,
                rx.vstack(
                    rx.text("Opciones", size="2", color=color_texto_secundario, weight="bold"),
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
                        rx.icon("check", size=16, color=color_exito),
                        rx.text("Respuesta correcta:", size="2", color=color_exito_oscuro, weight="bold"),
                        rx.text(pregunta.respuesta_correcta, size="2", color=color_exito_oscuro),
                        spacing="2",
                        align="center",
                    ),
                    padding="0.75em",
                    background_color=color_exito_fondo,
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
        border=f"1px solid {color_borde}",
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
            rx.text(estudiante.nombre, size="2", color=color_texto_principal, weight="bold"),
            rx.text(estudiante.correo, size="1", color=color_texto_gris),
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
        border_bottom=f"1px solid {color_fondo_claro}",
        align="center",
    )


def panel_detalles() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Información de la tarea", size="4", color=color_texto_principal),
            rx.text(MisTareasState.tarea_detalle.descripcion, color=color_texto_secundario, size="3", white_space="pre-wrap", line_height="1.6"),
            rx.divider(margin_y="0.75em"),
            rx.cond(
                MisTareasState.tarea_detalle.enunciado != "",
                rx.vstack(
                    rx.text("Enunciado", size="2", color=color_texto_secundario, weight="bold"),
                    rx.text(MisTareasState.tarea_detalle.enunciado, color=color_texto_terciario, size="2", white_space="pre-wrap", line_height="1.6"),
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
        border=f"1px solid {color_borde}",
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
                    rx.icon("circle-help", size=40, color=color_texto_claro),
                    rx.text("Esta tarea no tiene preguntas registradas.", color=color_texto_gris, size="2"),
                    align="center",
                ),
                width="100%",
                padding="3em",
            ),
        ),
        padding="1.5em",
        background_color="white",
        border=f"1px solid {color_borde}",
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
                    rx.icon("users-round", size=40, color=color_texto_claro),
                    rx.text("No hay estudiantes asignados a esta tarea.", color=color_texto_gris, size="2"),
                    align="center",
                ),
                width="100%",
                padding="3em",
            ),
        ),
        padding="1.5em",
        background_color="white",
        border=f"1px solid {color_borde}",
        border_radius="8px",
        border_top_left_radius="0",
    )


def contenido_detalle_tarea() -> rx.Component:
    return rx.cond(
        MisTareasState.error_detalle,
        rx.center(
            rx.vstack(
                rx.icon("file-warning", size=48, color=color_error),
                rx.heading("Tarea no encontrada", size="6", color=color_texto_principal),
                rx.text("La tarea no existe o no tienes permiso para verla.", color=color_texto_gris),
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
                color=color_texto_terciario,
                on_click=rx.redirect("/mis-tareas"),
                variant="ghost",
                color_scheme="gray",
                cursor="pointer",
                margin_bottom="0.5em",
            ),
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading(MisTareasState.tarea_detalle.titulo, size="8", weight="bold", color=color_texto_principal),
                        rx.badge(MisTareasState.tarea_detalle.tipo, color_scheme="indigo", variant="solid"),
                        spacing="3",
                        align="center",
                        flex_wrap="wrap",
                    ),
                    rx.text(MisTareasState.tarea_detalle.grupo, color=color_texto_terciario, size="3", weight="medium"),
                    align_items="start",
                    spacing="2",
                ),
                rx.spacer(),
                rx.cond(
                    MisTareasState.calificaciones_pendientes > 0,
                    rx.button(
                        rx.icon("send", size=16),
                        "Liberar calificaciones",
                        rx.badge(
                            MisTareasState.calificaciones_pendientes,
                            color_scheme="red",
                            variant="solid",
                            radius="full",
                        ),
                        variant="solid",
                        color_scheme="green",
                        cursor="pointer",
                        on_click=MisTareasState.liberar_calificaciones,
                    ),
                ),
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
                        rx.hstack(rx.icon("info", size=16, color=color_texto_principal), rx.text("Detalles", weight="bold", color=color_texto_principal)),
                        value="detalles",
                        cursor="pointer",
                        color=color_texto_principal,
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("circle-help", size=16, color=color_texto_principal), rx.text("Preguntas", weight="bold", color=color_texto_principal)),
                        value="preguntas",
                        cursor="pointer",
                        color=color_texto_principal,
                    ),
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("users", size=16, color=color_texto_principal), rx.text("Estudiantes", weight="bold", color=color_texto_principal)),
                        value="estudiantes",
                        cursor="pointer",
                        color=color_texto_principal,
                    ),
                    size="2",
                    background_color="white",
                    border=f"1px solid {color_borde}",
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
            background_color=color_fondo_pagina,
            overflow="auto",
        ),
        width="100%",
    )
