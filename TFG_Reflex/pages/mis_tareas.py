import reflex as rx
from ..state.mis_tareas_state import MisTareasState, TareaUI
from ..components.layout import sidebar_layout, header_component

def modal_confirmar_eliminacion() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Confirmar eliminación", color="#111827"),
            rx.dialog.description(
                f"Vas a eliminar la tarea '{MisTareasState.tarea_a_eliminar_titulo}'. Esta acción no se puede deshacer.",
                size="2",
                color="#4b5563",
                margin_bottom="1em",
            ),
            rx.text(
                "Para confirmar, escribe ",
                rx.text("ELIMINAR", weight="bold", color="#ef4444"),
                " en el cuadro de abajo:",
                size="2",
                color="#374151",
            ),
            rx.input(
                placeholder="ELIMINAR",
                value=MisTareasState.confirm_delete_input,
                on_change=MisTareasState.set_confirm_delete_input,
                margin_y="1em",
                width="100%",
                border="1px solid #d1d5db",
                background_color="white",
                color="#111827",
            ),
            rx.flex(
                rx.button(
                    "Cancelar",
                    variant="surface",
                    color_scheme="gray",
                    color="#374151",
                    on_click=MisTareasState.cambiar_estado_modal_eliminar(False),
                    cursor="pointer",
                ),
                rx.button(
                    "Eliminar Tarea",
                    on_click=MisTareasState.confirmar_eliminacion_tarea,
                    color_scheme="red",
                    disabled=MisTareasState.confirm_delete_input != "ELIMINAR",
                    cursor="pointer",
                ),
                spacing="3",
                justify="end",
                margin_top="1em",
            ),
            max_width="450px",
            background_color="white",
        ),
        open=MisTareasState.modal_eliminar_abierto,
        on_open_change=MisTareasState.cambiar_estado_modal_eliminar,
    )

def render_tarjeta_tarea(tarea: TareaUI) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(tarea.titulo, size="4", color="#111827", weight="bold"),
                rx.spacer(),
                rx.badge(tarea.grupo, color_scheme="indigo", size="2"),
                width="100%",
                align_items="center"
            ),
            
            rx.text(tarea.descripcion, size="2", color="#4b5563", line_clamp=2, margin_y="0.5em"),
            
            rx.hstack(
                rx.icon("calendar-days", size=16, color="#6b7280"),
                rx.text(tarea.fechas, size="2", color="#6b7280", weight="medium"),
                align_items="center",
                spacing="2"
            ),
            
            rx.divider(margin_y="1em"),
            
            rx.hstack(
                rx.button(
                    rx.icon("eye", size=16),
                    "Detalles",
                    variant="soft",
                    color_scheme="indigo",
                    size="2",
                    cursor="pointer",
                    on_click=MisTareasState.ver_detalles(tarea.id_tarea),
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("trash", size=16),
                    variant="ghost",
                    color_scheme="red",
                    size="2",
                    cursor="pointer",
                    on_click=MisTareasState.abrir_modal_eliminar(tarea.id_tarea, tarea.titulo),
                ),
                width="100%"
            ),
            spacing="2", width="100%", align_items="start"
        ),
        width="100%", padding="1.5em", border="1px solid #e5e7eb", background_color="white", _hover={"box_shadow": "md", "border_color": "#c7d2fe"}
    )

def mis_tareas_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Mis Tareas Creadas"),
                
                rx.cond(
                    MisTareasState.tareas,
                    rx.grid(
                        rx.foreach(MisTareasState.tareas, render_tarjeta_tarea),
                        columns="2",
                        spacing="5", 
                        width="100%",
                        margin_top="2em"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("folder-open", size=48, color="#9ca3af"),
                            rx.text("Aún no has creado ninguna tarea.", color="#6b7280", size="3", weight="medium"),
                            rx.link(
                                rx.button("Crear mi primera tarea", color_scheme="indigo", margin_top="1em"),
                                href="/crear-tarea"
                            ),
                            align_items="center"
                        ),
                        width="100%", height="40vh"
                    )
                ),
                
                modal_confirmar_eliminacion(),

                padding="3em", max_width="1000px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )
