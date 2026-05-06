import reflex as rx
from ..state.evaluar_tarea_state import EvaluarTareaState, RespuestaUI
from ..components.layout import sidebar_layout, header_component
from ..colores import *

def render_respuesta(respuesta: RespuestaUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(f"Pregunta {respuesta.numero}", color_scheme="indigo", variant="soft"),
                rx.badge(respuesta.tipo, color_scheme="gray", variant="surface"),
                width="100%",
                align="center",
                spacing="2",
            ),
            rx.text(respuesta.enunciado, color=color_texto_principal, size="3", white_space="pre-wrap", line_height="1.6", weight="medium"),
            
            rx.divider(margin_y="0.5em"),
            
            rx.text("Respuesta del alumno:", size="2", color=color_texto_secundario, weight="bold"),
            
            rx.cond(
                respuesta.respuesta_diagrama != "",
                rx.box(
                    rx.html(respuesta.respuesta_diagrama),
                    width="100%",
                    min_height="300px",
                    border=f"1px solid {color_borde}",
                    border_radius="8px",
                    background_color=color_fondo_pagina,
                    padding="1em",
                    overflow="auto",
                    display="flex",
                    justify_content="center",
                    align_items="center",
                ),
                rx.cond(
                    respuesta.respuesta_texto != "",
                    rx.box(
                        rx.text(respuesta.respuesta_texto, size="2", color=color_texto_principal, white_space="pre-wrap"),
                        width="100%",
                        padding="1em",
                        background_color=color_fondo_claro,
                        border_radius="8px",
                        border=f"1px solid {color_borde}",
                    ),
                    rx.text("El alumno no ha respondido a esta pregunta.", size="2", color=color_texto_claro, font_style="italic")
                )
            ),
            
            rx.divider(margin_y="0.5em"),
            
            rx.vstack(
                rx.hstack(
                    rx.text("Calificación:", size="2", color=color_texto_principal, weight="bold"),
                    rx.input(
                        type="number", 
                        min="0", max=respuesta.calificacion_maxima.to_string(), step="0.1",
                        value=respuesta.calificacion.to_string(),
                        on_change=lambda v: EvaluarTareaState.actualizar_calificacion(respuesta.id_pregunta, v),
                        width="100px",
                        border=f"1px solid {color_borde_input}",
                        background_color="white",
                        color=color_texto_principal,
                    ),
                    rx.text(f"/ {respuesta.calificacion_maxima}", size="2", color=color_texto_gris),
                    align="center", spacing="2"
                ),
                rx.text("Retroalimentación (opcional):", size="2", color=color_texto_principal, weight="bold"),
                rx.text_area(
                    placeholder="Escribe comentarios o sugerencias sobre la respuesta...",
                    value=respuesta.retroalimentacion,
                    on_change=lambda v: EvaluarTareaState.actualizar_retroalimentacion(respuesta.id_pregunta, v),
                    width="100%",
                    border=f"1px solid {color_borde_input}",
                    background_color="white",
                    color=color_texto_principal,
                ),
                spacing="2", width="100%"
            ),
            
            spacing="3",
            width="100%",
            align_items="start",
        ),
        width="100%",
        padding="1.5em",
        background_color="white",
        border=f"1px solid {color_borde}",
        box_shadow="sm",
    )

def contenido_evaluacion() -> rx.Component:
    return rx.cond(
        EvaluarTareaState.error_carga,
        rx.center(
            rx.vstack(
                rx.icon("file-warning", size=48, color=color_error),
                rx.heading("Resolución no encontrada", size="6", color=color_texto_principal),
                rx.text("No se pudo cargar la entrega del alumno o no tienes permiso para verla.", color=color_texto_gris),
                rx.button(
                    "Volver a mis tareas", 
                    on_click=rx.redirect("/mis-tareas"), 
                    color_scheme="indigo", 
                    cursor="pointer"
                ),
                align="center",
                spacing="3",
            ),
            width="100%",
            height="55vh",
        ),
        rx.vstack(
            rx.button(
                rx.icon("arrow-left", size=16),
                "Volver a los detalles de la tarea",
                color=color_texto_terciario,
                on_click=rx.redirect(f"/tarea/{EvaluarTareaState.id_tarea_actual}"),
                variant="ghost",
                color_scheme="gray",
                cursor="pointer",
                margin_bottom="0.5em",
            ),
            
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("file-check", size=24, color=color_primario),
                        rx.heading("Resolución de Tarea", size="6", color=color_texto_principal),
                        align="center",
                        spacing="2",
                    ),
                    rx.divider(margin_y="0.5em"),
                    rx.grid(
                        rx.box(
                            rx.text("Tarea", size="1", color=color_texto_gris, weight="bold"),
                            rx.text(EvaluarTareaState.titulo_tarea, size="3", color=color_texto_principal, weight="medium"),
                        ),
                        rx.box(
                            rx.text("Estudiante", size="1", color=color_texto_gris, weight="bold"),
                            rx.text(EvaluarTareaState.nombre_estudiante, size="3", color=color_texto_principal, weight="medium"),
                        ),
                        rx.box(
                            rx.text("Fecha de entrega", size="1", color=color_texto_gris, weight="bold"),
                            rx.text(EvaluarTareaState.fecha_entrega, size="3", color=color_texto_principal, weight="medium"),
                        ),
                        columns={"initial": "1", "sm": "3"},
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    spacing="3",
                ),
                padding="1.5em",
                background_color="white",
                border=f"1px solid {color_borde}",
                border_radius="8px",
                width="100%",
                margin_bottom="1.5em",
            ),
            
            rx.cond(
                EvaluarTareaState.respuestas.length() > 0,
                rx.vstack(
                    rx.foreach(EvaluarTareaState.respuestas, render_respuesta),
                    width="100%",
                    spacing="4",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("info", size=40, color=color_texto_claro),
                        rx.text("No se encontraron respuestas para esta tarea.", color=color_texto_gris, size="2"),
                        align="center",
                    ),
                    width="100%",
                    padding="3em",
                ),
            ),
            
            rx.box(
                rx.button(
                    rx.icon("circle-check", size=20),
                    "Calificar Tarea",
                    size="3",
                    color_scheme="green",
                    variant="solid",
                    cursor="pointer",
                    width="100%",
                    on_click=EvaluarTareaState.calificar_tarea,
                ),
                width="100%",
                padding="1.5em",
                margin_top="2em",
                background_color="white",
                border=f"1px solid {color_borde}",
                border_radius="8px",
                box_shadow="sm",
            ),
            
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding_bottom="3em",
        ),
    )

@rx.page(route="/evaluar-resolucion/[id_tarea]/[id_estudiante]", on_load=EvaluarTareaState.cargar_resolucion)
def evaluar_tarea_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Evaluar Resolución"),
                contenido_evaluacion(),
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
