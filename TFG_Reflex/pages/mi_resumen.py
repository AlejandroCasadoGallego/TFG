import reflex as rx
from ..components.layout import sidebar_layout, header_component
from ..state.informe_estudiante_state import InformeEstudianteState
from .informe_estudiante import stat_card, fila_tarea, grafico_evolucion
from ..colores import *


def mi_resumen_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),

                rx.box(
                    rx.hstack(
                        rx.button(
                            rx.icon("arrow-left", size=16),
                            "Volver al Dashboard",
                            on_click=rx.redirect("/dashboard"),
                            variant="ghost",
                            color_scheme="gray",
                            cursor="pointer",
                            margin_bottom="1em"
                        )
                    ),
                    rx.hstack(
                        rx.avatar(fallback=InformeEstudianteState.estudiante_nombre[:2].upper(), size="7", radius="full", color_scheme="indigo"),
                        rx.vstack(
                            rx.heading("Mi Resumen Académico", size="7", color=color_texto_principal, weight="bold"),
                            rx.text(InformeEstudianteState.estudiante_correo, size="3", color=color_texto_terciario),
                            align_items="start", spacing="2"
                        ),
                        spacing="5", align="center", width="100%", margin_bottom="2em"
                    ),

                    rx.grid(
                        stat_card("circle-check", "Tareas Evaluadas", InformeEstudianteState.total_completadas.to(str), color_exito_suave),
                        stat_card("graduation-cap", "Nota Media Global", InformeEstudianteState.nota_media.to(str), color_amarillo_suave),
                        columns={"initial": "1", "sm": "2"},
                        spacing="5",
                        width="100%",
                        margin_bottom="2em"
                    ),

                    grafico_evolucion(),

                    rx.card(
                        rx.vstack(
                            rx.text("Detalle de Evaluaciones", weight="bold", size="4", color=color_texto_principal),
                            rx.divider(margin_bottom="0.5em"),
                            rx.cond(
                                InformeEstudianteState.detalles_tareas.length() > 0,
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Tarea", color=color_texto_principal, weight="bold"),
                                            rx.table.column_header_cell("Fecha Entrega", color=color_texto_principal, weight="bold"),
                                            rx.table.column_header_cell("Calificación", color=color_texto_principal, weight="bold"),
                                            rx.table.column_header_cell("Comentarios del Docente", color=color_texto_principal, weight="bold"),
                                        ),
                                    ),
                                    rx.table.body(
                                        rx.foreach(InformeEstudianteState.detalles_tareas, fila_tarea)
                                    ),
                                    width="100%", variant="surface"
                                ),
                                rx.text("Aún no tienes tareas evaluadas.", color=color_texto_gris, margin_y="2em", font_style="italic")
                            ),
                            width="100%"
                        ),
                        padding="1.5em", width="100%", box_shadow="sm", border=f"1px solid {color_borde}", background_color="white"
                    ),

                    width="100%", max_width="1000px", margin="0 auto"
                ),
                padding="3em", width="100%"
            ),
            flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
        ),
        width="100%"
    )
