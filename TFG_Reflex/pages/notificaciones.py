import reflex as rx
from ..state.base_state import BaseState
from ..components.layout import sidebar_layout, header_component

def item_notificacion(notif: rx.Var) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    rx.cond(notif["leida"], "mail-open", "mail"),
                    color=rx.cond(notif["leida"], "#9ca3af", "#4f46e5")
                ),
                rx.vstack(
                    rx.heading(notif["titulo"], size="3", color="#111827"),
                    rx.text(notif["fecha"], size="1", color="#6b7280"),
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
                width="100%", align="center"
            ),
            rx.text(notif["mensaje"], size="2", color="#374151", margin_top="1em"),
            spacing="2",
            padding="1.5em",
        ),
        width="100%",
        background_color=rx.cond(notif["leida"], "#f9fafb", "white"),
        border="1px solid #e5e7eb",
        border_radius="8px",
        margin_bottom="1em",
        opacity=rx.cond(notif["leida"], "0.7", "1")
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
                            rx.icon("bell-off", size=48, color="#9ca3af"),
                            rx.text("No tienes notificaciones pendientes.", color="#6b7280"),
                            align="center", spacing="3", margin_top="5em"
                        ),
                        width="100%"
                    )
                ),
                padding="3em", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )