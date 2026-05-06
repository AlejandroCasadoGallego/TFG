import reflex as rx
from ..state.base_state import BaseState
from ..components.layout import sidebar_layout, header_component
from ..colores import *

def item_notificacion(notif: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    rx.cond(notif["leida"], "mail-open", "mail"),
                    color=rx.cond(notif["leida"], color_texto_claro, color_primario)
                ),
                rx.vstack(
                    rx.heading(notif["titulo"], size="3", color=color_texto_principal),
                    rx.hstack(
                        rx.text("De: ", size="1", color=color_texto_gris),
                        rx.text(notif["remitente_nombre"], size="1", color=color_primario, weight="bold"),
                        rx.text(" · ", size="1", color=color_borde_input),
                        rx.text(notif["fecha"], size="1", color=color_texto_gris),
                        spacing="1",
                        align="center",
                    ),
                    spacing="0"
                ),
                rx.spacer(),
                
                rx.cond(
                    ~notif["leida"],
                    rx.button(
                        "Marcar como leída", 
                        size="1", 
                        variant="soft", 
                        on_click=lambda: BaseState.marcar_como_leida(notif["id"]), 
                        cursor="pointer"
                    )
                ),

                rx.button(
                    rx.icon("reply", size=14),
                    "Responder",
                    size="1",
                    variant="soft",
                    color_scheme="indigo",
                    cursor="pointer",
                    on_click=lambda: BaseState.abrir_modal_respuesta(
                        notif["id"],
                        notif["remitente_id"],
                        notif["remitente_nombre"],
                        notif["titulo"],
                    ),
                ),
                
                rx.button(
                    rx.icon("trash-2", size=14),
                    size="1",
                    variant="ghost",
                    color_scheme="red",
                    cursor="pointer",
                    on_click=lambda: BaseState.eliminar_notificacion(notif["id"])
                ),
                
                width="100%", align="center"
            ),
            rx.text(notif["mensaje"], size="2", color=color_texto_secundario, margin_top="1em"),
            spacing="2",
            padding="1.5em",
        ),
        width="100%",
        background_color=rx.cond(notif["leida"], color_fondo_pagina, "white"),
        border=f"1px solid {color_borde}",
        border_radius="8px",
        margin_bottom="1em",
        opacity=rx.cond(notif["leida"], "0.7", "1")
    )


def modal_respuesta() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon("reply", size=20, color=color_primario),
                    rx.text("Responder mensaje", weight="bold"),
                    align="center",
                    spacing="2",
                ),
            ),
            rx.dialog.description(
                rx.vstack(
                    rx.hstack(
                        rx.text("Para:", size="2", color=color_texto_gris, weight="bold"),
                        rx.badge(BaseState.respuesta_remitente_nombre, color_scheme="indigo", variant="soft"),
                        align="center",
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Asunto:", size="2", color=color_texto_gris, weight="bold"),
                        rx.text(f"Re: {BaseState.respuesta_titulo_original}", size="2", color=color_texto_secundario),
                        align="center",
                        spacing="2",
                    ),
                    rx.divider(margin_y="0.5em"),
                    rx.text("Tu respuesta:", size="2", color=color_texto_secundario, weight="bold"),
                    rx.text_area(
                        placeholder="Escribe tu respuesta aquí...",
                        value=BaseState.respuesta_texto,
                        on_change=BaseState.set_respuesta_texto,
                        width="100%",
                        min_height="120px",
                        resize="vertical",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                                cursor="pointer",
                            ),
                        ),
                        rx.button(
                            rx.icon("send", size=14),
                            "Enviar Respuesta",
                            color_scheme="indigo",
                            cursor="pointer",
                            on_click=BaseState.enviar_respuesta,
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                        margin_top="0.5em",
                    ),
                    spacing="3",
                    width="100%",
                ),
            ),
            max_width="500px",
        ),
        open=BaseState.modal_respuesta_abierto,
        on_open_change=BaseState.cerrar_modal_respuesta,
    )


def notificaciones_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Centro de Notificaciones"),
                
                rx.cond(
                    BaseState.lista_notificaciones.length() > 0,
                    rx.vstack(
                        rx.foreach(BaseState.lista_notificaciones, item_notificacion),
                        width="100%", max_width="800px"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("bell-off", size=48, color=color_texto_claro),
                            rx.text("No tienes notificaciones pendientes.", color=color_texto_gris),
                            align="center", spacing="3", margin_top="5em"
                        ),
                        width="100%"
                    )
                ),
                modal_respuesta(),
                padding="3em", width="100%"
            ),
            flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
        ),
        width="100%"
    )