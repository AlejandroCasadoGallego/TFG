import reflex as rx
from ..state.resolver_tarea_state import ResolverTareaState
from ..state.resolver_tarea_state import ResolverTareaState, PreguntaResolucionUI
from ..components.diagram_board import diagram_board

def locked_header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("library-big", size=28, color="#4f46e5"),
            rx.heading("PatternLab", size="6", weight="bold", color="#111827"),
            align="center",
            spacing="3",
        ),
        padding="1em 2em",
        border_bottom="1px solid #e5e7eb",
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
                rx.button("Sí, Entregar", on_click=lambda: ResolverTareaState.finalizar_tarea(False), color_scheme="indigo", cursor="pointer"),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
    )

def renderizar_pregunta(pregunta: PreguntaResolucionUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(f"Pregunta", size="4", color="#374151", margin_bottom="0.5em"),
            rx.card(
                rx.markdown(pregunta.enunciado, color="#111827"),
                background_color="#f8fafc",
                padding="1em",
                margin_bottom="1em",
                width="100%",
                border_left="4px solid #4f46e5",
                color="#111827"
            ),
            
            rx.box(
                
                rx.box(
                    rx.text_area(
                        placeholder="Escribe tu respuesta detallada aquí...",
                        value=ResolverTareaState.respuestas[pregunta.id],
                        on_change=lambda val: ResolverTareaState.set_respuesta(pregunta.id, val),
                        width="100%",
                        min_height="200px",
                        border="1px solid #d1d5db",
                        color="#111827"
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
                        value=ResolverTareaState.respuestas[pregunta.id],
                        on_change=lambda val: ResolverTareaState.set_respuesta(pregunta.id, val),
                        direction="column",
                        spacing="3",
                        size="3",
                        color_scheme="gray",
                        style={"color": "#111827", "fontWeight": "500"}
                    ),
                    display=rx.cond(
                        (pregunta.tipo == "Test") | (pregunta.tipo == "test"),
                        "block", "none"
                    ),
                    width="100%"
                ),
                
                
                rx.box(
                    diagram_board(
                        on_diagram_change=lambda elements: ResolverTareaState.set_diagrama(pregunta.id, elements),
                        initial_data=ResolverTareaState.respuestas[pregunta.id],
                        height="600px",
                        width="100%"
                    ),
                    height="600px",
                    width="100%",
                    border="2px solid #e5e7eb",
                    border_radius="8px",
                    overflow="hidden",
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
        border="1px solid #e5e7eb"
    )

def resolver_tarea_page() -> rx.Component:
    return rx.box(
        locked_header(),
        
        
        rx.cond(
            ResolverTareaState.es_prueba,
            rx.box(
                rx.hstack(
                    rx.icon("timer", size=24, color=rx.cond(ResolverTareaState.tiempo_restante_segundos < 60, "#ef4444", "#f59e0b")),
                    rx.text("Tiempo Restante:", weight="bold", color="#374151"),
                    rx.heading(
                        ResolverTareaState.tiempo_formateado,
                        size="6",
                        color=rx.cond(ResolverTareaState.tiempo_restante_segundos < 60, "#ef4444", "#f59e0b")
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
                border_bottom="1px solid #e5e7eb",
                box_shadow="sm"
            )
        ),

        rx.box(
            rx.cond(
                ResolverTareaState.error_carga != "",
                rx.center(
                    rx.vstack(
                        rx.icon("triangle-alert", size=48, color="#ef4444"),
                        rx.heading("Error", size="6"),
                        rx.text(ResolverTareaState.error_carga, color="#6b7280"),
                        rx.button("Volver", on_click=rx.redirect("/mis-tareas-estudiante"), margin_top="1em", cursor="pointer"),
                        align="center",
                        spacing="3"
                    ),
                    padding="5em"
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(ResolverTareaState.tarea_actual.titulo, size="8", weight="bold", color="#111827"),
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
                                rx.heading("Descripción General", size="4", color="#374151"),
                                rx.text(ResolverTareaState.tarea_actual.descripcion, color="#4b5563", margin_bottom="1em"),
                                align_items="start"
                            ),
                            background_color="white",
                            padding="1.5em",
                            margin_bottom="1em",
                            width="100%",
                            border="1px solid #e5e7eb",
                            box_shadow="sm"
                        )
                    ),
                    
                    rx.cond(
                        ResolverTareaState.tarea_actual.enunciado != "",
                        rx.card(
                            rx.vstack(
                                rx.heading("Instrucciones y Requisitos", size="4", color="#374151"),
                                rx.markdown(ResolverTareaState.tarea_actual.enunciado),
                                align_items="start"
                            ),
                            background_color="#f3f4f6",
                            padding="1.5em",
                            margin_bottom="2em",
                            width="100%",
                            border="1px solid #e5e7eb",
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
            background_color="#f9fafb",
            min_height="calc(100vh - 80px)"
        )
    )
