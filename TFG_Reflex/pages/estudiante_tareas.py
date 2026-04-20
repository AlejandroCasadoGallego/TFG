import reflex as rx
from ..state.estudiante_tareas_state import EstudianteTareasState, EstudianteTareaUI
from ..components.layout import sidebar_layout, header_component

def tarjeta_tarea(tarea: EstudianteTareaUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.match(
                    tarea.tipo,
                    ("Ejercicio", rx.icon("clipboard-list", color="#4f46e5", size=24)),
                    ("Prueba", rx.icon("file-check", color="#4f46e5", size=24)),
                    rx.icon("file-text", color="#4f46e5", size=24)
                ),
                rx.heading(tarea.titulo, size="5", weight="bold", color="#111827"),
                rx.spacer(),
                rx.badge(tarea.tipo, color_scheme="indigo", variant="soft"),
                rx.badge(tarea.estado, color_scheme=rx.cond(tarea.estado.lower() == "pendiente", "orange", "green"), variant="soft"),
                align="center",
                spacing="3",
                width="100%"
            ),
            rx.divider(margin_y="0.5em"),
            rx.text(tarea.descripcion, size="2", color="#4b5563", margin_bottom="1em"),
            rx.cond(
                tarea.tipo != "Ejercicio",
                rx.hstack(
                    rx.icon("calendar", size=16, color="#6b7280"),
                    rx.text(tarea.fechas, size="2", color="#6b7280", weight="medium"),
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
        border="1px solid #e5e7eb",
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
                        rx.heading("Mis Tareas", size="8", weight="bold", color="#111827"),
                        rx.text("Tareas que tienes asignadas y que aún están en plazo.", color="#6b7280", size="3"),
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
                            rx.icon("circle-check", size=48, color="#9ca3af"),
                            rx.text("No tienes tareas pendientes.", weight="bold", color="#374151"),
                            rx.text("Todas tus tareas están completadas o han caducado.", color="#6b7280", size="2"),
                            align="center", spacing="2"
                        ),
                        padding="5em",
                        width="100%",
                        background_color="#ffffff",
                        border="2px dashed #e5e7eb",
                        border_radius="8px"
                    )
                ),
                
                padding="3em", max_width="1000px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )
