import reflex as rx
from ..state.base_state import BaseState
from ..components.layout import sidebar_layout, header_component
from ..colores import *


def seccion_relacion(titulo: str, icono_desc: str, instrucciones: list[str], color: str = color_primario) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.box(width="8px", height="8px", border_radius="full", background_color=color),
                rx.heading(titulo, size="4", weight="bold", color=color_texto_principal),
                align="center", spacing="2"
            ),
            rx.text(icono_desc, size="2", color=color_texto_gris, style={"fontStyle": "italic"}),
            rx.divider(margin_y="0.5em"),
            rx.vstack(
                *[rx.hstack(
                    rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"),
                    rx.text(paso, size="2", color=color_texto_secundario),
                    align="start", spacing="2"
                ) for paso in instrucciones],
                spacing="2", width="100%"
            ),
            spacing="3", width="100%", align_items="start"
        ),
        width="100%",
        padding="1.5em",
        background_color="white",
        border=f"1px solid {color_borde}",
        box_shadow="sm",
    )


def seccion_clase() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("square", size=20, color=color_primario),
                rx.heading("Representación de una Clase", size="5", weight="bold", color=color_texto_principal),
                align="center", spacing="2"
            ),
            rx.text("Para representar una clase UML en la pizarra, sigue estos pasos:", size="2", color=color_texto_gris),
            rx.divider(margin_y="0.5em"),

            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("1", size="2", weight="bold", color="white"),
                        background_color=color_primario,
                        width="24px", height="24px", border_radius="full",
                        display="flex", align_items="center", justify_content="center"
                    ),
                    rx.text("Dibujar el contorno de la clase", size="3", weight="bold", color=color_texto_principal),
                    align="center", spacing="2"
                ),
                rx.text('Selecciona la herramienta "Rectángulo" (□) de la barra inferior. Dibuja un rectángulo que será el contenedor de tu clase.', size="2", color=color_texto_secundario, padding_left="2em"),
                spacing="1", width="100%"
            ),

            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("2", size="2", weight="bold", color="white"),
                        background_color=color_primario,
                        width="24px", height="24px", border_radius="full",
                        display="flex", align_items="center", justify_content="center"
                    ),
                    rx.text("Nombre de la clase", size="3", weight="bold", color=color_texto_principal),
                    align="center", spacing="2"
                ),
                rx.text('Usa la herramienta "Texto" (T) y escribe el nombre de la clase en la parte SUPERIOR del rectángulo.', size="2", color=color_texto_secundario, padding_left="2em"),
                spacing="1", width="100%"
            ),

            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("3", size="2", weight="bold", color="white"),
                        background_color=color_primario,
                        width="24px", height="24px", border_radius="full",
                        display="flex", align_items="center", justify_content="center"
                    ),
                    rx.text("Separadores internos", size="3", weight="bold", color=color_texto_principal),
                    align="center", spacing="2"
                ),
                rx.text('Usa la herramienta "Flecha", seleccionando como final "Ninguno" (—) para dibujar líneas horizontales dentro del rectángulo, dividiendo en 3 secciones: Nombre | Atributos | Operaciones.', size="2", color=color_texto_secundario, padding_left="2em"),
                spacing="1", width="100%"
            ),

            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("4", size="2", weight="bold", color="white"),
                        background_color=color_primario,
                        width="24px", height="24px", border_radius="full",
                        display="flex", align_items="center", justify_content="center"
                    ),
                    rx.text("Atributos y operaciones", size="3", weight="bold", color=color_texto_principal),
                    align="center", spacing="2"
                ),
                rx.text('Usa "Texto" (T) para escribir los atributos en la sección central y las operaciones en la sección inferior.', size="2", color=color_texto_secundario, padding_left="2em"),
                rx.box(
                    rx.vstack(
                        rx.text("Ejemplo de clase dibujada en la pizarra:", size="2", weight="bold", color=color_texto_secundario, margin_bottom="0.5em"),
                        rx.image(
                            src="/uml_class_example.png",
                            alt="Ejemplo de clase UML dibujada en la pizarra",
                            max_width="400px",
                            width="100%",
                            border_radius="8px",
                            border=f"1px solid {color_borde}",
                        ),
                        align_items="center", width="100%"
                    ),
                    margin_left="2em",
                    margin_top="0.5em"
                ),
                spacing="1", width="100%"
            ),
            spacing="4", width="100%", align_items="start"
        ),
        width="100%",
        padding="2em",
        background_color="white",
        border=f"1px solid {color_borde}",
        box_shadow="sm"
    )


def _standalone_header() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("library-big", size=28, color=color_primario),
            rx.heading("PatternLab", size="6", weight="bold", color=color_texto_principal),
            align="center", spacing="3",
        ),
        rx.spacer(),
        rx.text("Leyenda de Diagramas UML", size="3", color=color_texto_gris, weight="medium"),
        padding="1em 2em",
        border_bottom=f"1px solid {color_borde}",
        background_color="white",
        width="100%",
        align_items="center"
    )


def _contenido_leyenda() -> rx.Component:
    return rx.vstack(
        rx.card(
            rx.hstack(
                rx.icon("info", size=24, color=color_primario),
                rx.vstack(
                    rx.text("Esta guía te muestra cómo representar los elementos de un diagrama de clases UML usando las herramientas disponibles en la pizarra.", size="2", color=color_texto_secundario),
                    rx.text("Consulta esta leyenda siempre que necesites recordar cómo dibujar una relación o clase.", size="2", color=color_texto_gris),
                    spacing="1"
                ),
                align="start", spacing="3"
            ),
            background_color=color_indigo_fondo,
            border=f"1px solid {color_indigo_borde}",
            padding="1.5em",
            width="100%",
            margin_bottom="1em"
        ),
        rx.heading("Herramientas de la Pizarra", size="6", weight="bold", color=color_texto_principal, margin_top="1em", margin_bottom="0.5em"),
        rx.text("A continuación se muestran las herramientas que necesitarás para dibujar los diagramas UML.", size="2", color=color_texto_gris, margin_bottom="1em"),

        rx.grid(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_primario),
                        rx.heading("Crear Texto", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text('Selecciona la herramienta "Texto" (T) de la barra inferior para escribir nombres de clases, atributos y operaciones.', size="2", color=color_texto_gris),
                    rx.divider(margin_y="0.5em"),
                    rx.center(
                        rx.image(src="/Texto.png", alt="Herramienta Texto", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                        width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%", height="100%", padding="1.5em", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm",
            ),

            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_info),
                        rx.heading("Crear Flecha", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text('Selecciona la herramienta "Flecha" (↗) de la barra inferior para dibujar las relaciones entre las clases del diagrama.', size="2", color=color_texto_gris),
                    rx.divider(margin_y="0.5em"),
                    rx.center(
                        rx.image(src="/Flecha.png", alt="Herramienta Flecha", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                        width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%", height="100%", padding="1.5em", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm",
            ),

            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_morado),
                        rx.heading("Punta de Flecha", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text("Tras seleccionar una flecha, elige el tipo de punta (Final) desde el panel derecho.", size="2", color=color_texto_gris),
                    rx.divider(margin_y="0.5em"),
                    rx.center(
                        rx.image(src="/Punta de flecha.png", alt="Seleccionar punta de flecha", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                        width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%", height="100%", padding="1.5em", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm",
            ),

            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_advertencia),
                        rx.heading("Tipo de Raya", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text("Cambia entre línea sólida y discontinua desde el panel derecho.", size="2", color=color_texto_gris),
                    rx.divider(margin_y="0.5em"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Sólida", size="1", weight="bold", color=color_texto_secundario),
                            rx.image(src="/Raya --- Dibujar.png", alt="Raya — Dibujar", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                            align_items="center", spacing="1"
                        ),
                        rx.icon("arrow-right", size=20, color=color_primario, flex_shrink="0"),
                        rx.vstack(
                            rx.text("Discontinua", size="1", weight="bold", color=color_texto_secundario),
                            rx.image(src="/Raya --- Discontínua.png", alt="Raya — Discontinua", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                            align_items="center", spacing="1"
                        ),
                        align="center", spacing="3", justify="center", width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%", height="100%", padding="1.5em", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm",
            ),

            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_error),
                        rx.heading("Relleno", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text("Cambia el relleno de una forma para simular diamantes rellenos (Composición).", size="2", color=color_texto_gris),
                    rx.divider(margin_y="0.5em"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Sin relleno", size="1", weight="bold", color=color_texto_secundario),
                            rx.image(src="/Relleno --- Ninguno.png", alt="Relleno — Ninguno", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                            align_items="center", spacing="1"
                        ),
                        rx.icon("arrow-right", size=20, color=color_primario, flex_shrink="0"),
                        rx.vstack(
                            rx.text("Con relleno", size="1", weight="bold", color=color_texto_secundario),
                            rx.image(src="/Relleno --- Relleno.png", alt="Relleno — Relleno", border_radius="6px", border=f"1px solid {color_borde}", style={"imageRendering": "-webkit-optimize-contrast"}),
                            align_items="center", spacing="1"
                        ),
                        align="center", spacing="3", justify="center", width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%", height="100%", padding="1.5em", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm",
            ),

            columns=rx.breakpoints(initial="1", sm="2", md="3"),
            spacing="4",
            width="100%"
        ),

        rx.heading("Clases UML", size="6", weight="bold", color=color_texto_principal, margin_top="2em", margin_bottom="0.5em"),
        seccion_clase(),

        rx.heading("Relaciones UML", size="6", weight="bold", color=color_texto_principal, margin_top="2em", margin_bottom="0.5em"),
        rx.text("Todas las relaciones se dibujan usando la herramienta Flecha (↗) de la barra inferior. Después, ajusta el tipo de línea y la punta desde el panel derecho.", size="2", color=color_texto_gris, margin_bottom="1em"),

        rx.grid(
            seccion_relacion("Asociación", "Relación genérica entre dos clases.", [
                'Selecciona la herramienta "Flecha" (↗) de la barra inferior.',
                "Dibuja una línea de una clase a otra.",
                'En el panel derecho ("Raya"), asegúrate de que la raya sea de tipo Dibujar (—).',
                'El final de la flecha debe ser una FLECHA normal (→), el final por defecto.',
            ], color_primario),
            seccion_relacion("Herencia (Generalización)", "Una clase hija extiende una clase padre.", [
                'Selecciona la herramienta "Flecha" (↗).',
                "Dibuja de la clase hija a la clase padre.",
                'Raya de tipo Raya Dibujar (—).',
                'Final: TRIÁNGULO (▷) desde el panel "Puntas de flecha".',
            ], color_info),
            seccion_relacion("Implementación", "Una clase implementa una interfaz.", [
                'Selecciona la herramienta "Flecha" (↗).',
                "Dibuja de la clase a la interfaz.",
                'Cambia la raya a de tipo Discontinua (- - -) en el panel derecho ("Raya").',
                'Final: TRIÁNGULO (▷).',
            ], color_morado),
            seccion_relacion("Dependencia", "Una clase usa temporalmente a otra.", [
                'Selecciona la herramienta "Flecha" (↗).',
                "Dibuja de la clase dependiente a la clase usada.",
                'Cambia la raya a de tipo Discontinua (- - -) en el panel derecho ("Raya").',
                'El final debe ser una FLECHA normal (→).',
            ], color_advertencia),
            seccion_relacion("Agregación", "Relación 'tiene un' (el todo puede existir sin las partes).", [
                'Selecciona la herramienta "Flecha" (↗).',
                "Dibuja de la parte al todo.",
                'Raya de tipo Dibujar (—).',
                'Final: DIAMANTE (◇) desde "Puntas de flecha".',
                "El diamante queda HUECO por defecto, lo cual es correcto.",
            ], color_exito),
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(width="8px", height="8px", border_radius="full", background_color=color_error),
                        rx.heading("Composición", size="4", weight="bold", color=color_texto_principal),
                        align="center", spacing="2"
                    ),
                    rx.text("Relación 'tiene un' fuerte (las partes no existen sin el todo).", size="2", color=color_texto_gris, style={"fontStyle": "italic"}),
                    rx.divider(margin_y="0.5em"),
                    rx.vstack(
                        rx.hstack(rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"), rx.text('Selecciona la herramienta "Flecha" (↗).', size="2", color=color_texto_secundario), align="start", spacing="2"),
                        rx.hstack(rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"), rx.text("Dibuja de la parte al todo.", size="2", color=color_texto_secundario), align="start", spacing="2"),
                        rx.hstack(rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"), rx.text('Raya SÓLIDA (—).', size="2", color=color_texto_secundario), align="start", spacing="2"),
                        rx.hstack(rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"), rx.text('Final: DIAMANTE (◇) desde "Puntas de flecha".', size="2", color=color_texto_secundario), align="start", spacing="2"),
                        rx.hstack(rx.box(width="6px", height="6px", border_radius="full", background_color=color_primario, flex_shrink="0", margin_top="6px"), rx.text("Para simular el diamante RELLENO, cambia el relleno a el tipo Relleno - Relleno", size="2", color=color_texto_secundario), align="start", spacing="2"),
                        spacing="2", width="100%"
                    ),
                    spacing="3", width="100%", align_items="start"
                ),
                width="100%",
                padding="1.5em",
                background_color="white",
                border=f"1px solid {color_borde}",
                box_shadow="sm",
            ),
            columns=rx.breakpoints(initial="1", sm="1", md="2"),
            spacing="4",
            width="100%"
        ),

        rx.heading("Resumen Rápido", size="6", weight="bold", color=color_texto_principal, margin_top="2em", margin_bottom="0.5em"),
        rx.card(
            rx.vstack(
                rx.text("Referencia visual de los tipos de flecha disponibles en la pizarra:", size="2", color=color_texto_secundario, margin_bottom="0.5em"),
                rx.center(
                    rx.image(
                        src="/uml_arrows_legend.png",
                        alt="Leyenda de flechas UML: Asociación, Herencia, Implementación, Dependencia, Agregación, Composición",
                        max_width="500px",
                        width="100%",
                    ),
                    width="100%"
                ),
                spacing="2", width="100%", align_items="start"
            ),
            background_color="white", padding="2em", border=f"1px solid {color_borde}", box_shadow="sm", width="100%"
        ),

        padding="3em",
        max_width="1100px",
        margin="0 auto",
        width="100%",
        padding_bottom="5em"
    )


def leyenda_diagramas_page() -> rx.Component:
    return rx.cond(
        BaseState.usuario_actual != "",
        rx.flex(
            sidebar_layout(),
            rx.box(
                rx.vstack(
                    header_component("Leyenda de Diagramas UML"),
                    _contenido_leyenda(),
                ),
                flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
            ),
            width="100%"
        ),
        rx.box(
            _standalone_header(),
            rx.box(
                _contenido_leyenda(),
                background_color=color_fondo_pagina,
                min_height="calc(100vh - 60px)",
                overflow="auto"
            ),
            width="100%"
        ),
    )
