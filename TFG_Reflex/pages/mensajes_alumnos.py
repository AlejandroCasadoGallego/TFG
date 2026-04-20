import reflex as rx
from ..state.mensajes_state import MensajesState, EstudianteDestinatarioUI
from ..components.layout import sidebar_layout, header_component


def render_estudiante_seleccionable(estudiante: EstudianteDestinatarioUI) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.avatar(
                fallback=estudiante.nombre[:2].upper(),
                size="2",
                radius="full",
                color_scheme="indigo",
            ),
            rx.vstack(
                rx.text(estudiante.nombre, size="2", color="#111827", weight="bold"),
                rx.text(estudiante.correo, size="1", color="#6b7280"),
                spacing="0",
                align_items="start",
            ),
            rx.spacer(),
            rx.cond(
                MensajesState.destinatario_seleccionado == estudiante.id_estudiante,
                rx.icon("circle-check", size=18, color="#4f46e5"),
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        padding="0.75em 1em",
        border_radius="8px",
        cursor="pointer",
        background_color=rx.cond(
            MensajesState.destinatario_seleccionado == estudiante.id_estudiante,
            "#f5f3ff",
            "transparent",
        ),
        border=rx.cond(
            MensajesState.destinatario_seleccionado == estudiante.id_estudiante,
            "2px solid #4f46e5",
            "1px solid #e5e7eb",
        ),
        _hover={"background_color": "#f5f3ff", "border_color": "#a5b4fc"},
        on_click=MensajesState.seleccionar_destinatario(
            estudiante.id_estudiante, estudiante.nombre
        ),
        transition="all 0.15s ease",
    )


def render_mensaje_enviado(msg: rx.Var) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(
                rx.cond(msg["leida"], "mail-open", "mail"),
                size=18,
                color=rx.cond(msg["leida"], "#9ca3af", "#4f46e5"),
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(msg["titulo"], size="2", color="#111827", weight="bold"),
                    rx.spacer(),
                    rx.text(msg["fecha"], size="1", color="#9ca3af"),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    rx.cond(msg["leida"], "Leído", "No leído"),
                    size="1",
                    color=rx.cond(msg["leida"], "#16a34a", "#d97706"),
                    weight="medium",
                ),
                rx.text(
                    "Para: ",
                    rx.text.strong(msg["destinatario"]),
                    size="1",
                    color="#6b7280",
                ),
                rx.text(msg["mensaje"], size="1", color="#4b5563", no_of_lines=2),
                spacing="1",
                width="100%",
                align_items="start",
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        padding="1em 1.25em",
        background_color=rx.cond(msg["leida"], "#f9fafb", "white"),
        border="1px solid #e5e7eb",
        border_radius="8px",
        opacity=rx.cond(msg["leida"], "0.75", "1"),
    )


def panel_redactar() -> rx.Component:
    return rx.box(
        rx.vstack(
            
            rx.hstack(
                rx.icon("pen-line", size=20, color="#4f46e5"),
                rx.heading("Redactar Mensaje", size="4", color="#111827"),
                align="center",
                spacing="2",
            ),
            rx.divider(margin_y="0.5em"),

            
            rx.text("Destinatario", size="2", color="#374151", weight="bold"),
            rx.cond(
                MensajesState.destinatario_nombre != "",
                rx.hstack(
                    rx.badge(
                        rx.hstack(
                            rx.icon("user", size=12),
                            rx.text(MensajesState.destinatario_nombre),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="indigo",
                        variant="soft",
                        size="2",
                    ),
                    rx.button(
                        rx.icon("x", size=14),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                        cursor="pointer",
                        on_click=MensajesState.seleccionar_destinatario("", ""),
                    ),
                    align="center",
                    spacing="2",
                ),
                rx.text(
                    "Selecciona un alumno de la lista...",
                    size="1",
                    color="#9ca3af",
                    font_style="italic",
                ),
            ),

            
            rx.input(
                placeholder="Buscar alumno por nombre o correo...",
                value=MensajesState.busqueda_estudiante,
                on_change=MensajesState.set_busqueda_estudiante,
                width="100%",
            ),
            rx.scroll_area(
                rx.vstack(
                    rx.cond(
                        MensajesState.estudiantes_filtrados.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                MensajesState.estudiantes_filtrados,
                                render_estudiante_seleccionable,
                            ),
                            width="100%",
                            spacing="2",
                        ),
                        rx.center(
                            rx.text(
                                "No se encontraron alumnos.",
                                size="2",
                                color="#9ca3af",
                            ),
                            padding="2em",
                            width="100%",
                        ),
                    ),
                    width="100%",
                ),
                type="hover",
                style={"max_height": "220px"},
                width="100%",
            ),

            rx.divider(margin_y="0.5em"),

            
            rx.text("Asunto", size="2", color="#374151", weight="bold"),
            rx.input(
                placeholder="Escribe el asunto del mensaje...",
                value=MensajesState.titulo_mensaje,
                on_change=MensajesState.set_titulo_mensaje,
                width="100%",
            ),
            rx.text("Mensaje", size="2", color="#374151", weight="bold"),
            rx.text_area(
                placeholder="Escribe tu mensaje aquí...",
                value=MensajesState.cuerpo_mensaje,
                on_change=MensajesState.set_cuerpo_mensaje,
                width="100%",
                min_height="150px",
                resize="vertical",
            ),

            
            rx.button(
                rx.icon("send", size=16),
                "Enviar Mensaje",
                color_scheme="indigo",
                width="100%",
                cursor="pointer",
                size="3",
                on_click=MensajesState.enviar_mensaje,
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        padding="1.5em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        width="100%",
    )


def panel_historial() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("history", size=20, color="#4f46e5"),
                rx.heading("Mensajes Enviados", size="4", color="#111827"),
                align="center",
                spacing="2",
            ),
            rx.divider(margin_y="0.5em"),
            rx.cond(
                MensajesState.mensajes_enviados.length() > 0,
                rx.vstack(
                    rx.foreach(
                        MensajesState.mensajes_enviados, render_mensaje_enviado
                    ),
                    width="100%",
                    spacing="2",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("mail-x", size=40, color="#9ca3af"),
                        rx.text(
                            "Aún no has enviado ningún mensaje.",
                            color="#6b7280",
                            size="2",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    width="100%",
                    padding="3em",
                ),
            ),
            spacing="3",
            width="100%",
            align_items="start",
        ),
        padding="1.5em",
        background_color="white",
        border="1px solid #e5e7eb",
        border_radius="8px",
        width="100%",
    )


def contenido_mensajes() -> rx.Component:
    return rx.vstack(
        rx.grid(
            panel_redactar(),
            panel_historial(),
            columns={"initial": "1", "lg": "2"},
            spacing="5",
            width="100%",
        ),
        width="100%",
        max_width="1200px",
        margin="0 auto",
    )


def mensajes_alumnos_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Mensajes a Alumnos"),
                contenido_mensajes(),
                width="100%",
                padding="3em",
            ),
            flex="1",
            height="100vh",
            background_color="#f9fafb",
            overflow="auto",
        ),
        width="100%",
    )
