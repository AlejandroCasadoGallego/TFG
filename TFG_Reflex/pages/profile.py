import reflex as rx
from ..state.profile_state import ProfileState
from ..components.layout import sidebar_layout, header_component

def perfil_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(),
                rx.container(
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.avatar(fallback=ProfileState.usuario_actual[:2], size="7", radius="full", color_scheme="indigo"),
                                rx.vstack(
                                    rx.heading(ProfileState.datos_perfil["nombre"], size="7", color="#111827", weight="bold"),
                                    rx.badge(ProfileState.usuario_rol.upper(), color_scheme="indigo", variant="solid"),
                                    align_items="start", spacing="1"
                                ),
                                spacing="5", align="center", width="100%", margin_bottom="1em"
                            ),
                            rx.divider(size="4", margin_y="1em"),
                            rx.vstack(
                                rx.text("Detalles de la Cuenta", weight="bold", size="4", color="#111827", margin_bottom="0.5em"),
                                rx.grid(
                                    rx.text("Email:", weight="bold", color="#4b5563"), rx.text(ProfileState.datos_perfil["correo"], color="#1f2937"),
                                    rx.text("ID de Usuario:", weight="bold", color="#4b5563"), rx.text(f"#{ProfileState.datos_perfil['id']}", color="#1f2937"),
                                    columns="2", spacing="4", width="100%"
                                ),
                                align_items="start", width="100%", background_color="#f8fafc", padding="1.5em", border_radius="12px", border="1px solid #e2e8f0"
                            ),
                            rx.flex(
                                rx.button(
                                    rx.hstack(rx.icon("user-pen", size=18), rx.text("Editar Perfil", white_space="nowrap"), align="center", spacing="2"),
                                    on_click=ProfileState.preparar_edicion, color_scheme="indigo", size="3", variant="solid", cursor="pointer", flex="1"
                                ),
                                rx.dialog.root(
                                    rx.dialog.trigger(
                                        rx.button(
                                            rx.hstack(rx.icon("user-x", size=18), rx.text("Eliminar Cuenta", white_space="nowrap"), align="center", spacing="2"),
                                            color_scheme="red", size="3", variant="outline", cursor="pointer", flex="1", width="100%"
                                        )
                                    ),
                                    rx.dialog.content(
                                        rx.dialog.title("⚠️ Advertencia de Eliminación"),
                                        rx.dialog.description("Esta acción desactivará tu cuenta y cerrarás sesión inmediatamente.", margin_bottom="1em"),
                                        rx.text("Escribe la palabra ", rx.text("ELIMINAR", weight="bold", color="#ef4444"), " para confirmar:", size="2"),
                                        rx.input(placeholder="ELIMINAR", on_change=ProfileState.set_confirm_delete_input, margin_y="1em"),
                                        rx.flex(
                                            rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                                            rx.dialog.close(rx.button("Sí, deshabilitar mi cuenta", on_click=ProfileState.confirmar_eliminacion, color_scheme="red", disabled=ProfileState.confirm_delete_input != "ELIMINAR")),
                                            spacing="3", justify="end"
                                        ),
                                    )
                                ),
                                spacing="4", width="100%", margin_top="2em", flex_direction=["column", "row"]
                            ),
                        ),
                        padding="3em", width="100%", background_color="white", box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)", border="1px solid #e5e7eb"
                    ),
                    size="2"
                ),
                padding="3em", align="center", width="100%"
            ),
            flex="1", height="100vh", background_color="#f3f4f6", overflow="auto"
        ),
        width="100%"
    )

def editar_perfil_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Editar Perfil", size="7", color="#111827", weight="bold"),
                rx.text("Modifica tu información personal.", color="#6b7280", size="2", margin_bottom="1.5em"),
                
                rx.vstack(
                    rx.text("Nombre Completo", weight="bold", size="2", color="#374151", width="100%"),
                    rx.input(value=ProfileState.edit_nombre, on_change=ProfileState.set_edit_nombre, width="100%", color="#111827", background_color="white", border="1px solid #d1d5db"),
                    
                    rx.text("Correo Electrónico", weight="bold", size="2", color="#374151", width="100%", margin_top="0.5em"),
                    rx.input(value=ProfileState.edit_correo, on_change=ProfileState.set_edit_correo, width="100%", color="#111827", background_color="white", border="1px solid #d1d5db"),
                    
                    rx.text("Nueva Contraseña (dejar en blanco para mantener)", weight="bold", size="2", color="#374151", width="100%", margin_top="0.5em"),
                    rx.input(type="password", placeholder="••••••••", value=ProfileState.edit_pass, on_change=ProfileState.set_edit_pass, width="100%", color="#111827", background_color="white", border="1px solid #d1d5db"),
                    spacing="3", width="100%"
                ),

                rx.cond(ProfileState.error_edicion != "", rx.text(ProfileState.error_edicion, color="#ef4444", size="2", weight="medium", margin_top="1em")),
                
                rx.grid(
                    rx.button("Cancelar", on_click=rx.redirect("/perfil"), background_color="#f3f4f6", color="#374151", border="1px solid #d1d5db", width="100%", cursor="pointer"),
                    rx.button("Guardar Cambios", on_click=ProfileState.guardar_cambios_perfil, background_color="#4f46e5", color="white", width="100%", cursor="pointer"),
                    columns="2", spacing="4", width="100%", margin_top="2em"
                ),
                align="center", width="100%"
            ),
            padding="2.5em", width="450px", background_color="white", box_shadow="xl", border="1px solid #e5e7eb"
        ),
        height="100vh", background_color="#f3f4f6"
    )