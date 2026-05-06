import reflex as rx
from ..state.resolver_tarea_state import ResolverTareaState
from ..state.resolver_tarea_state import ResolverTareaState, PreguntaResolucionUI
from ..components.diagram_board import diagram_board
from ..colores import *

def locked_header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("library-big", size=28, color=color_primario),
            rx.heading("PatternLab", size="6", weight="bold", color=color_texto_principal),
            align="center",
            spacing="3",
        ),
        padding="1em 2em",
        border_bottom=f"1px solid {color_borde}",
        background_color="white",
        width="100%",
        align_items="center"
    )

def modal_confirmar_entrega() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Finalizar Tarea",
                color_scheme="indigo",
                size="4",
                cursor="pointer",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Confirmar Entrega"),
            rx.dialog.description(
                
                
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray", cursor="pointer")
                ),
                rx.button("Sí, Entregar", on_click=ResolverTareaState.finalizar_tarea(False), color_scheme="indigo", cursor="pointer"),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
    )

def renderizar_pregunta(pregunta: PreguntaResolucionUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(f"Pregunta", size="4", color=color_texto_secundario, margin_bottom="0.5em"),
            rx.card(
                rx.markdown(pregunta.enunciado, color=color_texto_principal),
                background_color=color_fondo_hover,
                padding="1em",
                margin_bottom="1em",
                width="100%",
                border_left=f"4px solid {color_primario}",
                color=color_texto_principal
            ),
            
            rx.box(
                
                rx.box(
                    rx.text_area(
                        placeholder="Escribe tu respuesta detallada aquí...",
                        value=pregunta.respuesta_actual,
                        on_change=lambda val: ResolverTareaState.set_respuesta(pregunta.id, val),
                        width="100%",
                        min_height="200px",
                        border=f"1px solid {color_borde_input}",
                        color=color_texto_principal
                    ),
                    display=rx.cond(
                        (pregunta.tipo == "Desarrollo") | (pregunta.tipo == "desarrollo"),
                        "block", "none"
                    ),
                    width="100%"
                ),
                
                
                rx.box(
                    rx.radio(
                        pregunta.opciones,
                        value=pregunta.respuesta_actual,
                        on_change=lambda val: ResolverTareaState.set_respuesta(pregunta.id, val),
                        direction="column",
                        spacing="3",
                        size="3",
                        color_scheme="gray",
                        style={"color": color_texto_principal, "fontWeight": "500"}
                    ),
                    display=rx.cond(
                        (pregunta.tipo == "Test") | (pregunta.tipo == "test"),
                        "block", "none"
                    ),
                    width="100%"
                ),
                
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    rx.hstack(
                                        rx.icon("book-open", size=16),
                                        rx.text("Ver Leyenda UML"),
                                        align="center", spacing="2"
                                    ),
                                    variant="outline",
                                    color_scheme="indigo",
                                    size="2",
                                    cursor="pointer",
                                ),
                                href="/leyenda-diagramas",
                                is_external=True,
                            ),
                            width="100%",
                            justify="end",
                        ),
                        rx.box(
                            diagram_board(
                                on_diagram_change=lambda elements: ResolverTareaState.set_diagrama(pregunta.id, elements),
                                initial_data=pregunta.respuesta_actual,
                                height="600px",
                                width="100%"
                            ),
                            height="600px",
                            width="100%",
                            border=f"2px solid {color_borde}",
                            border_radius="8px",
                            overflow="hidden",
                        ),
                        spacing="2", width="100%"
                    ),
                    width="100%",
                    display=rx.cond(
                        (pregunta.tipo == "Diagrama") | (pregunta.tipo == "diagrama"),
                        "block", "none"
                    )
                ),
                
                
                rx.text(
                    f"Tipo de pregunta no soportado: ", pregunta.tipo, color="red",
                    display=rx.cond(
                        (pregunta.tipo != "Desarrollo") & (pregunta.tipo != "desarrollo") &
                        (pregunta.tipo != "Test") & (pregunta.tipo != "test") &
                        (pregunta.tipo != "Diagrama") & (pregunta.tipo != "diagrama"),
                        "block", "none"
                    )
                ),
                width="100%"
            ),
            width="100%",
            align_items="start"
        ),
        width="100%",
        padding="2em",
        margin_bottom="2em",
        background_color="white",
        box_shadow="sm",
        border=f"1px solid {color_borde}"
    )

def resolver_tarea_page() -> rx.Component:
    return rx.box(
        locked_header(),
        
        
        rx.cond(
            ResolverTareaState.es_prueba,
            rx.box(
                rx.hstack(
                    rx.icon("timer", size=24, color=rx.cond(ResolverTareaState.tiempo_restante_segundos < 60, color_error, color_amarillo_suave)),
                    rx.text("Tiempo Restante:", weight="bold", color=color_texto_secundario),
                    rx.heading(
                        ResolverTareaState.tiempo_formateado,
                        size="6",
                        color=rx.cond(ResolverTareaState.tiempo_restante_segundos < 60, color_error, color_amarillo_suave)
                    ),
                    spacing="3",
                    align="center",
                    justify="center"
                ),
                position="sticky",
                top="0",
                z_index="50",
                background_color="white",
                padding="1em",
                border_bottom=f"1px solid {color_borde}",
                box_shadow="sm"
            )
        ),

        rx.box(
            rx.cond(
                ResolverTareaState.error_carga != "",
                rx.center(
                    rx.vstack(
                        rx.icon("triangle-alert", size=48, color=color_error),
                        rx.heading("Error", size="6"),
                        rx.text(ResolverTareaState.error_carga, color=color_texto_gris),
                        rx.button("Volver", on_click=rx.redirect("/mis-tareas-estudiante"), margin_top="1em", cursor="pointer"),
                        align="center",
                        spacing="3"
                    ),
                    padding="5em"
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(ResolverTareaState.tarea_actual.titulo, size="8", weight="bold", color=color_texto_principal),
                        rx.spacer(),
                        modal_confirmar_entrega(),
                        width="100%",
                        align="center",
                        margin_bottom="1em"
                    ),
                    
                    rx.cond(
                        ResolverTareaState.tarea_actual.descripcion != "",
                        rx.card(
                            rx.vstack(
                                rx.heading("Descripción General", size="4", color=color_texto_secundario),
                                rx.text(ResolverTareaState.tarea_actual.descripcion, color=color_texto_terciario, margin_bottom="1em"),
                                align_items="start"
                            ),
                            background_color="white",
                            padding="1.5em",
                            margin_bottom="1em",
                            width="100%",
                            border=f"1px solid {color_borde}",
                            box_shadow="sm"
                        )
                    ),
                    
                    rx.cond(
                        ResolverTareaState.tarea_actual.enunciado != "",
                        rx.card(
                            rx.vstack(
                                rx.heading("Instrucciones y Requisitos", size="4", color=color_texto_secundario),
                                rx.markdown(ResolverTareaState.tarea_actual.enunciado),
                                align_items="start"
                            ),
                            background_color=color_fondo_claro,
                            padding="1.5em",
                            margin_bottom="2em",
                            width="100%",
                            border=f"1px solid {color_borde}",
                            box_shadow="sm"
                        )
                    ),
                    
                    rx.foreach(
                        ResolverTareaState.preguntas,
                        renderizar_pregunta
                    ),
                    
                    rx.box(
                        modal_confirmar_entrega(),
                        width="100%",
                        text_align="right",
                        margin_top="2em"
                    ),
                    
                    width="100%",
                    max_width="900px",
                    margin="0 auto",
                    padding_y="3em",
                    align_items="start"
                )
            ),
            padding_x="2em",
            background_color=color_fondo_pagina,
            min_height="calc(100vh - 80px)"
        )
    )
