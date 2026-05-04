import reflex as rx
from ..state.ver_correccion_state import VerCorreccionState, RespuestaCorregidaUI
from ..components.layout import sidebar_layout, header_component

def render_respuesta_corregida(respuesta: RespuestaCorregidaUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(f"Pregunta {respuesta.numero}", color_scheme="indigo", variant="soft"),
                rx.badge(respuesta.tipo, color_scheme="gray", variant="surface"),
                rx.spacer(),
                rx.badge(f"{respuesta.calificacion} / {respuesta.calificacion_maxima} pts", color_scheme="green", variant="solid"),
                width="100%",
                align="center",
                spacing="2",
            ),
            rx.text(respuesta.enunciado, color="#111827", size="3", white_space="pre-wrap", line_height="1.6", weight="medium"),
            
            rx.divider(margin_y="0.5em"),
            
            rx.text("Tu respuesta:", size="2", color="#374151", weight="bold"),
            
            rx.cond(
                respuesta.respuesta_diagrama != "",
                rx.box(
                    rx.html(respuesta.respuesta_diagrama),
                    width="100%",
                    min_height="300px",
                    border="1px solid #e5e7eb",
                    border_radius="8px",
                    background_color="#f9fafb",
                    padding="1em",
                    overflow="auto",
                    display="flex",
                    justify_content="center",
                    align_items="center",
                ),
                rx.cond(
                    respuesta.respuesta_texto != "",
                    rx.box(
                        rx.text(respuesta.respuesta_texto, size="2", color="#111827", white_space="pre-wrap"),
                        width="100%",
                        padding="1em",
                        background_color="#f3f4f6",
                        border_radius="8px",
                        border="1px solid #e5e7eb",
                    ),
                    rx.text("No has respondido a esta pregunta.", size="2", color="#9ca3af", font_style="italic")
                )
            ),
            
            rx.divider(margin_y="0.5em"),
            
            rx.vstack(
                rx.text("Comentarios del profesor:", size="2", color="#111827", weight="bold"),
                rx.box(
                    rx.text(respuesta.retroalimentacion, size="2", color="#111827", white_space="pre-wrap"),
                    width="100%",
                    padding="1em",
                    background_color="#f0fdf4",
                    border_radius="8px",
                    border="1px solid #bbf7d0",
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
        border="1px solid #e5e7eb",
        box_shadow="sm",
    )

def contenido_correccion() -> rx.Component:
    return rx.cond(
        VerCorreccionState.error_carga,
        rx.center(
            rx.vstack(
                rx.icon("file-warning", size=48, color="#ef4444"),
                rx.heading("Corrección no encontrada", size="6", color="#111827"),
                rx.text("No se pudo cargar la corrección o aún no ha sido evaluada.", color="#6b7280"),
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
                "Volver a mis tareas",
                color="#4b5563",
                on_click=rx.redirect("/mis-tareas"),
                variant="ghost",
                color_scheme="gray",
                cursor="pointer",
                margin_bottom="0.5em",
            ),
            
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("award", size=28, color="#10b981"),
                        rx.heading("Corrección: " + VerCorreccionState.titulo_tarea, size="7", color="#111827"),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(VerCorreccionState.descripcion_tarea, color="#4b5563", size="3"),
                    rx.divider(margin_y="0.5em"),
                    rx.grid(
                        rx.box(
                            rx.text("Fecha de entrega", size="1", color="#6b7280", weight="bold"),
                            rx.text(VerCorreccionState.fecha_entrega, size="3", color="#111827", weight="medium"),
                        ),
                        rx.box(
                            rx.text("Calificación Total", size="1", color="#6b7280", weight="bold"),
                            rx.badge(
                                f"{VerCorreccionState.calificacion_total} / {VerCorreccionState.calificacion_maxima_total}",
                                size="3",
                                color_scheme="green",
                                variant="solid"
                            ),
                        ),
                        columns={"initial": "1", "sm": "2"},
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    spacing="3",
                ),
                padding="1.5em",
                background_color="white",
                border="1px solid #e5e7eb",
                border_radius="8px",
                width="100%",
                margin_bottom="1.5em",
            ),
            
            rx.cond(
                VerCorreccionState.respuestas.length() > 0,
                rx.vstack(
                    rx.foreach(VerCorreccionState.respuestas, render_respuesta_corregida),
                    width="100%",
                    spacing="4",
                ),
                rx.center(
                    rx.text("No se encontraron respuestas para esta tarea.", color="#6b7280", size="2"),
                    width="100%",
                    padding="3em",
                ),
            ),
            
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding_bottom="3em",
        ),
    )


def ver_correccion_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Ver Corrección"),
                contenido_correccion(),
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
