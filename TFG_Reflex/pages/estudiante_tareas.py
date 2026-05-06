import reflex as rx
from ..state.estudiante_tareas_state import EstudianteTareasState, EstudianteTareaUI
from ..components.layout import sidebar_layout, header_component
from ..colores import *

def tarjeta_tarea(tarea: EstudianteTareaUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.match(
                        tarea.tipo,
                        ("Ejercicio", rx.icon("clipboard-list", color=color_primario, size=24)),
                        ("Prueba", rx.icon("file-check", color=color_primario, size=24)),
                        rx.icon("file-text", color=color_primario, size=24)
                    ),
                    rx.heading(tarea.titulo, size="5", weight="bold", color=color_texto_principal, style={"word_break": "break-word"}),
                    align="center",
                    spacing="3",
                    min_width="0",
                    flex="1",
                ),
                rx.hstack(
                    rx.badge(tarea.tipo, color_scheme="indigo", variant="soft"),
                    rx.badge(tarea.estado, color_scheme=rx.cond(tarea.estado.lower() == "pendiente", "orange", "green"), variant="soft"),
                    spacing="2",
                    flex_shrink="0",
                ),
                align="center",
                spacing="3",
                width="100%",
                flex_wrap="wrap",
            ),
            rx.divider(margin_y="0.5em"),
            rx.text(tarea.descripcion, size="2", color=color_texto_terciario, margin_bottom="1em"),
            rx.cond(
                tarea.tipo != "Ejercicio",
                rx.hstack(
                    rx.icon("calendar", size=16, color=color_texto_gris),
                    rx.text(tarea.fechas, size="2", color=color_texto_gris, weight="medium"),
                    spacing="2",
                    align="center"
                )
            ),
            rx.box(
                rx.button(
                    "Realizar Tarea",
                    on_click=lambda: EstudianteTareasState.ir_a_tarea(tarea.id_tarea),
                    color_scheme="indigo",
                    width="100%",
                    margin_top="1em",
                    cursor="pointer"
                )
            ),
            align_items="start",
            width="100%"
        ),
        width="100%",
        box_shadow="sm",
        border=f"1px solid {color_borde}",
        background_color="white",
        padding="1.5em"
    )

def estudiante_tareas_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Mis Tareas", size="8", weight="bold", color=color_texto_principal),
                        rx.text("Tareas que tienes asignadas y que aún están en plazo.", color=color_texto_gris, size="3"),
                    ),
                    rx.spacer(),
                    width="100%", align="center", margin_bottom="2em"
                ),
                
                rx.cond(
                    EstudianteTareasState.tareas.length() > 0,
                    rx.grid(
                        rx.foreach(EstudianteTareasState.tareas, tarjeta_tarea),
                        columns={"initial": "1", "sm": "2", "md": "3"},
                        spacing="5",
                        width="100%"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("circle-check", size=48, color=color_texto_claro),
                            rx.text("No tienes tareas pendientes.", weight="bold", color=color_texto_secundario),
                            rx.text("Todas tus tareas están completadas o han caducado.", color=color_texto_gris, size="2"),
                            align="center", spacing="2"
                        ),
                        padding="5em",
                        width="100%",
                        background_color=color_fondo_blanco,
                        border=f"2px dashed {color_borde}",
                        border_radius="8px"
                    )
                ),
                
                rx.divider(margin_y="2em"),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Tareas Corregidas", size="6", weight="bold", color=color_texto_principal),
                        rx.text("Tareas que ya han sido evaluadas por tu profesor.", color=color_texto_gris, size="3"),
                    ),
                    rx.spacer(),
                    width="100%", align="center", margin_bottom="1em"
                ),
                
                rx.cond(
                    EstudianteTareasState.tareas_corregidas.length() > 0,
                    rx.grid(
                        rx.foreach(EstudianteTareasState.tareas_corregidas, lambda t: rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("file-check", color=color_exito_suave, size=24),
                                    rx.heading(t.titulo, size="5", weight="bold", color=color_texto_principal),
                                    rx.spacer(),
                                    rx.badge("Corregida", color_scheme="green", variant="soft"),
                                    align="center",
                                    spacing="3",
                                    width="100%"
                                ),
                                rx.divider(margin_y="0.5em"),
                                rx.text(t.descripcion, size="2", color=color_texto_terciario, margin_bottom="1em"),
                                rx.box(
                                    rx.button(
                                        "Ver Corrección",
                                        on_click=lambda: EstudianteTareasState.ir_a_correccion(t.id_tarea),
                                        color_scheme="green",
                                        variant="soft",
                                        width="100%",
                                        margin_top="1em",
                                        cursor="pointer"
                                    )
                                ),
                                align_items="start",
                                width="100%"
                            ),
                            width="100%",
                            box_shadow="sm",
                            border=f"1px solid {color_exito_suave}",
                            background_color=color_exito_fondo,
                            padding="1.5em"
                        )),
                        columns={"initial": "1", "sm": "2", "md": "3"},
                        spacing="5",
                        width="100%"
                    ),
                    rx.text("Aún no tienes tareas corregidas.", color=color_texto_gris, font_style="italic")
                ),
                
                padding="3em", max_width="1000px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
        ),
        width="100%"
    )
