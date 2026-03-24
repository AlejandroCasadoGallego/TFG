import reflex as rx
from ..state.estudiante_grupos_state import EstudianteGruposState
from ..models.usuarios import Grupos
from ..components.layout import sidebar_layout, header_component

def modal_unirse_grupo() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(rx.icon("user-plus", size=18), "Unirse a Grupo", color_scheme="indigo", cursor="pointer")
        ),
        rx.dialog.content(
            rx.dialog.title("Unirse a un Grupo", color="#111827"),
            rx.dialog.description("Introduce el código de 6 caracteres proporcionado por tu profesor.", size="2", color="#4b5563"),
            
            rx.vstack(
                rx.text("Código de acceso *", weight="bold", size="2", color="#374151"),
                rx.input(
                    placeholder="Ej: A7X9WQ",
                    on_change=EstudianteGruposState.set_codigo_input,
                    value=EstudianteGruposState.codigo_input,
                    width="100%",
                    border="1px solid #d1d5db", 
                    background_color="white", 
                    color="#111827",
                    max_length=10
                ),
                rx.cond(
                    EstudianteGruposState.error_union != "",
                    rx.text(EstudianteGruposState.error_union, color="#ef4444", size="2", weight="medium")
                ),
                spacing="3",
                width="100%",
                margin_top="1em"
            ),
            
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="surface", color_scheme="gray", color="#374151", on_click=EstudianteGruposState.limpiar_formulario, cursor="pointer")
                ),
                rx.dialog.close(
                    rx.button("Unirse", on_click=EstudianteGruposState.unirse_grupo, color_scheme="indigo", color="white", cursor="pointer")
                ),
                spacing="3",
                margin_top="2em",
                justify="end",
            ),
            max_width="450px",
            background_color="white"
        )
    )

def tarjeta_grupo(grupo: Grupos) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("users", color="#4f46e5", size=24),
                rx.heading(grupo.nombre, size="5", weight="bold", color="#111827"),
                align="center",
                spacing="3"
            ),
            rx.divider(margin_y="0.5em"),
            rx.text("Te has unido al grupo correctamente.", size="2", color="#16a34a", weight="medium"),
            spacing="3",
            align_items="start"
        ),
        width="100%",
        box_shadow="sm",
        border="1px solid #e5e7eb",
        background_color="white"
    )

def estudiante_grupos_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Mis Grupos", size="8", weight="bold", color="#111827"),
                        rx.text("Aquí aparecen los grupos a los que perteneces.", color="#6b7280", size="3"),
                    ),
                    rx.spacer(),
                    modal_unirse_grupo(),
                    width="100%", align="center", margin_bottom="2em"
                ),
                
                rx.cond(
                    EstudianteGruposState.mis_grupos.length() > 0,
                    rx.grid(
                        rx.foreach(EstudianteGruposState.mis_grupos, tarjeta_grupo),
                        columns={"initial": "1", "sm": "2", "md": "3"},
                        spacing="5",
                        width="100%"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("users", size=48, color="#9ca3af"),
                            rx.text("Aún no perteneces a ningún grupo.", weight="bold", color="#374151"),
                            rx.text("Pídele el código a tu profesor y únete.", color="#6b7280", size="2"),
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