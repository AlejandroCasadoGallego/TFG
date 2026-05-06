import reflex as rx
from ..state.admin_state import AdminState
from ..components.layout import sidebar_layout, header_component
from ..colores import *


def fila_usuario_reset(usuario: dict) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=usuario["nombre"][:2].upper(), size="2", radius="full", color_scheme="indigo"),
        rx.vstack(
            rx.text(usuario["nombre"], weight="bold", size="2", color=color_texto_principal),
            rx.text(usuario["correo"], size="1", color=color_texto_gris),
            spacing="0",
            align_items="start",
        ),
        rx.spacer(),
        rx.badge(usuario["rol"], color_scheme=rx.cond(usuario["rol"] == "Docente", "blue", "green"), variant="soft"),
        rx.button(
            rx.icon("key-round", size=14),
            "Resetear",
            size="1",
            variant="soft",
            color_scheme="red",
            cursor="pointer",
            on_click=AdminState.abrir_modal_reset(usuario["id"], usuario["nombre"]),
        ),
        width="100%",
        padding="0.9em 0",
        border_bottom=f"1px solid {color_fondo_claro}",
        align="center",
    )


def modal_reset_password() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Resetear Contraseña"),
            rx.dialog.description(
                rx.text(
                    "Establece una nueva contraseña para ",
                    rx.text(AdminState.reset_usuario_nombre, as_="span", weight="bold"),
                    ". El usuario deberá cambiarla al iniciar sesión.",
                    color=color_texto_terciario,
                ),
            ),
            rx.vstack(
                rx.text("Nueva contraseña", size="2", weight="bold", color=color_texto_secundario),
                rx.input(
                    placeholder="Mínimo 6 caracteres",
                    type="password",
                    value=AdminState.reset_nueva_pass,
                    on_change=AdminState.set_reset_nueva_pass,
                    width="100%",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", color_scheme="gray", cursor="pointer"),
                    ),
                    rx.button(
                        "Confirmar Reset",
                        color_scheme="red",
                        cursor="pointer",
                        on_click=AdminState.confirmar_reset_password,
                    ),
                    spacing="3",
                    width="100%",
                    justify="end",
                    margin_top="1em",
                ),
                spacing="3",
                width="100%",
                margin_top="1em",
            ),
        ),
        open=AdminState.modal_reset_abierto,
        on_open_change=AdminState.cerrar_modal_reset,
    )


def resetear_contrasenas_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Resetear Contraseñas"),

                rx.vstack(
                    rx.hstack(
                        rx.icon("key-round", size=28, color=color_error),
                        rx.vstack(
                            rx.heading("Gestión de Contraseñas", size="6", weight="bold", color=color_texto_principal),
                            rx.text("Busca un usuario y establece una nueva contraseña temporal.", color=color_texto_gris, size="3"),
                            spacing="1",
                        ),
                        spacing="4",
                        align="center",
                        width="100%",
                        margin_bottom="1.5em",
                    ),

                    rx.input(
                        rx.input.slot(rx.icon("search", size=16)),
                        placeholder="Buscar por nombre o correo...",
                        value=AdminState.busqueda_reset,
                        on_change=AdminState.set_busqueda_reset,
                        width="100%",
                        margin_bottom="1em",
                    ),

                    rx.card(
                        rx.cond(
                            AdminState.usuarios_reset_filtrados.length() > 0,
                            rx.vstack(
                                rx.foreach(AdminState.usuarios_reset_filtrados, fila_usuario_reset),
                                width="100%",
                                spacing="0",
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.icon("user-x", size=40, color=color_texto_claro),
                                    rx.text("No se encontraron usuarios.", color=color_texto_gris, size="2"),
                                    align="center",
                                ),
                                width="100%",
                                padding="3em",
                            ),
                        ),
                        width="100%",
                        padding="1.5em",
                        box_shadow="sm",
                        border=f"1px solid {color_borde}",
                        background_color="white",
                    ),

                    modal_reset_password(),

                    width="100%",
                    max_width="800px",
                    margin="0 auto",
                ),

                padding="3em",
                width="100%",
            ),
            flex="1",
            height="100vh",
            background_color=color_fondo_pagina,
            overflow="auto",
        ),
        width="100%",
    )
