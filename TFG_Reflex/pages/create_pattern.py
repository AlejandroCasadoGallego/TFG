import reflex as rx
from ..state.base_state import BaseState
from ..state.patterns_state import PatternsState
from ..components.layout import sidebar_layout, header_component
from ..colores import *

def create_pattern_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Crear Nuevo Patrón", size="8", weight="bold", color=color_texto_principal),
                        rx.text("Añade un nuevo patrón de diseño al catálogo interactivo.", color=color_texto_gris, size="3"),
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("arrow-left", size=18), "Volver a la Biblioteca", 
                        on_click=rx.redirect("/biblioteca"), variant="ghost", color_scheme="gray", cursor="pointer"
                    ),
                    width="100%", align="center", margin_bottom="2em"
                ),
                
                rx.card(
                    rx.vstack(
                        rx.grid(
                            rx.vstack(
                                rx.text("Nombre del Patrón *", weight="bold", size="2", color=color_texto_secundario),
                                rx.input(placeholder="Ej: Singleton", value=PatternsState.nuevo_nombre, on_change=PatternsState.set_nuevo_nombre, width="100%", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            rx.vstack(
                                rx.text("Categoría *", weight="bold", size="2", color=color_texto_secundario),
                                rx.select(
                                    ["Creacionales", "Estructurales", "De Comportamiento"],
                                    value=PatternsState.nueva_categoria,
                                    on_change=PatternsState.set_nueva_categoria,
                                    width="100%"
                                ),
                                width="100%"
                            ),
                            columns="2", spacing="5", width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text("Descripción Breve *", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(placeholder="Escribe un resumen de qué hace este patrón...", value=PatternsState.nueva_descripcion, on_change=PatternsState.set_nueva_descripcion, width="100%", height="100px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Diagrama UML (Imagen)", weight="bold", size="2", color=color_texto_secundario),
                            rx.upload(
                                rx.vstack(
                                    rx.button("Seleccionar o arrastrar imagen", color_scheme="indigo", variant="outline"),
                                    rx.text("Arrastra un archivo PNG o JPG aquí.", color=color_texto_gris, size="1"),
                                    align="center", justify="center", padding="2em", border=f"2px dashed {color_borde_input}", border_radius="8px", background_color=color_fondo_pagina, width="100%", cursor="pointer"
                                ),
                                id="upload_diagrama",
                                multiple=False,
                                accept={
                                    "image/png": [".png"],
                                    "image/jpeg": [".jpg", ".jpeg"]
                                },
                                max_files=1
                            ),

                            rx.cond(
                                rx.selected_files("upload_diagrama").length() > 0,
                                rx.hstack(
                                    rx.icon("image", color=color_exito, size=18),
                                    rx.text("Archivo listo para subir: ", weight="bold", size="2", color=color_exito_oscuro),
                                    rx.foreach(rx.selected_files("upload_diagrama"), lambda file: rx.text(file, size="2", color=color_exito_check)),
                                    rx.spacer(),
                                    rx.button(
                                        rx.icon("trash-2", size=16),
                                        on_click=rx.clear_selected_files("upload_diagrama"),
                                        variant="ghost", color_scheme="red", size="1", cursor="pointer"
                                    ),
                                    align="center", width="100%", padding="0.75em 1em", background_color=color_exito_fondo_claro, border_radius="6px", border="1px solid #bbf7d0"
                                ),
                                rx.text("Ninguna imagen seleccionada", color=color_texto_claro, size="1", margin_top="0.2em")
                            ),
                            
                            width="100%", margin_top="1em"
                        ),
                        
                        rx.divider(margin_y="2em"),
                        rx.heading("Detalles Teóricos (Opcional)", size="5", weight="bold", color=color_texto_principal),
                        
                        rx.grid(
                            rx.vstack(
                                rx.text("Ventajas", weight="bold", size="2", color=color_texto_secundario),
                                rx.text_area(value=PatternsState.nuevas_ventajas, on_change=PatternsState.set_nuevas_ventajas, width="100%", height="150px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            rx.vstack(
                                rx.text("Desventajas", weight="bold", size="2", color=color_texto_secundario),
                                rx.text_area(value=PatternsState.nuevas_desventajas, on_change=PatternsState.set_nuevas_desventajas, width="100%", height="150px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            columns="2", spacing="5", width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Ejemplos de Uso", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(placeholder="Ej: Se usa en bases de datos, loggers...", value=PatternsState.nuevos_ejemplos, on_change=PatternsState.set_nuevos_ejemplos, width="100%", height="100px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Pseudocódigo", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(placeholder="Pega aquí el código...", value=PatternsState.nuevo_pseudocodigo, on_change=PatternsState.set_nuevo_pseudocodigo, width="100%", height="200px", style={"font_family": "monospace"}, border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),
                        
                        rx.cond(
                            PatternsState.error_creacion != "",
                            rx.text(PatternsState.error_creacion, color=color_error, size="2", weight="medium", margin_top="1em")
                        ),

                        rx.button(
                            "Crear Patrón", 
                            on_click=PatternsState.handle_upload(rx.upload_files(upload_id="upload_diagrama")),
                            color_scheme="indigo", size="4", width="100%", margin_top="2em", cursor="pointer"
                        ),

                        width="100%", padding="2em", align_items="start"
                    ),
                    width="100%", background_color="white", border=f"1px solid {color_borde}", box_shadow="sm"
                ),
                padding="3em", max_width="1000px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
        ),
        width="100%"
    )