import reflex as rx
from ..components.layout import sidebar_layout, header_component
from ..state.informe_estudiante_state import InformeEstudianteState
from ..colores import *

def stat_card(icon: str, title: str, value: str, color: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.icon(icon, size=24, color=color),
                padding="0.75em",
                border_radius="12px",
                background_color=f"{color}20",
            ),
            rx.vstack(
                rx.text(title, size="2", color=color_texto_gris, weight="medium"),
                rx.heading(value, size="6", color=color_texto_principal, weight="bold"),
                spacing="1"
            ),
            spacing="4",
            align="center"
        ),
        padding="1.5em",
        width="100%",
        box_shadow="sm",
        border=f"1px solid {color_borde}",
        background_color="white"
    )

def fila_tarea(tarea: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.vstack(
                rx.text(tarea["titulo"], weight="bold", color=color_texto_principal),
                rx.text(tarea["tipo"], size="1", color=color_texto_gris),
                spacing="1"
            )
        ),
        rx.table.cell(rx.text(tarea["fecha"], color=color_texto_secundario)),
        rx.table.cell(
            rx.badge(
                tarea["calificacion"], 
                color_scheme=rx.cond(tarea["aprobado"], "green", "red"),
                variant="solid"
            )
        ),
        rx.table.cell(
            rx.text(tarea["comentarios"], color=color_texto_terciario, size="2")
        ),
    )

def grafico_evolucion() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text("Evolución Temporal del Rendimiento", weight="bold", size="4", color=color_texto_principal),
            rx.divider(margin_bottom="1em"),
            rx.cond(
                InformeEstudianteState.datos_grafico.length() > 0,
                rx.recharts.line_chart(
                    rx.recharts.line(
                        data_key="calificacion",
                        stroke=color_primario,
                        stroke_width=2,
                        active_dot={"r": 8}
                    ),
                    rx.recharts.x_axis(data_key="nombre"),
                    rx.recharts.y_axis(domain=[0, 10]),
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(),
                    data=InformeEstudianteState.datos_grafico,
                    width="100%",
                    height=300,
                ),
                rx.center(
                    rx.text("No hay datos suficientes para generar la gráfica.", color=color_texto_gris, font_style="italic"),
                    height="300px", width="100%"
                )
            ),
            width="100%"
        ),
        padding="1.5em",
        width="100%",
        box_shadow="sm",
        border=f"1px solid {color_borde}",
        background_color="white",
        margin_bottom="2em"
    )

def informe_estudiante_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.box(
                    rx.hstack(
                        rx.button(
                            rx.icon("arrow-left", size=16),
                            "Volver a Mis Grupos",
                            on_click=rx.redirect("/mis-grupos"),
                            variant="ghost",
                            color_scheme="gray",
                            cursor="pointer",
                            margin_bottom="1em"
                        )
                    ),
                    rx.hstack(
                        rx.avatar(fallback=InformeEstudianteState.estudiante_nombre[:2].upper(), size="7", radius="full", color_scheme="indigo"),
                        rx.vstack(
                            rx.heading(InformeEstudianteState.estudiante_nombre, size="7", color=color_texto_principal, weight="bold"),
                            rx.text(InformeEstudianteState.estudiante_correo, size="3", color=color_texto_terciario),
                            rx.badge("Estudiante", color_scheme="indigo", variant="soft"),
                            align_items="start", spacing="2"
                        ),
                        spacing="5", align="center", width="100%", margin_bottom="2em"
                    ),
                    
                    rx.grid(
                        stat_card("circle-check", "Ejercicios Completados", InformeEstudianteState.total_completadas.to(str), color_exito_suave),
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
                                rx.text("El estudiante aún no tiene tareas evaluadas.", color=color_texto_gris, margin_y="2em", font_style="italic")
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
