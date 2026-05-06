import reflex as rx
from ..state.base_state import BaseState
from ..state.edit_pattern_state import EditPatternState
from ..components.layout import sidebar_layout, header_component
from ..colores import *

def edit_pattern_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Modificar Patrón", size="8", weight="bold", color=color_texto_principal),
                        rx.text("Edita los detalles de este patrón de diseño.", color=color_texto_gris, size="3"),
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("arrow-left", size=18), "Cancelar", 
                        on_click=rx.redirect(f"/patron/{EditPatternState.router.page.params.get('id_patron', '')}"), 
                        variant="ghost", color_scheme="gray", cursor="pointer"
                    ),
                    width="100%", align="center", margin_bottom="2em"
                ),
                
                rx.card(
                    rx.vstack(
                        rx.grid(
                            rx.vstack(
                                rx.text("Nombre del Patrón *", weight="bold", size="2", color=color_texto_secundario),
                                rx.input(value=EditPatternState.edit_nombre, on_change=EditPatternState.set_edit_nombre, width="100%", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            rx.vstack(
                                rx.text("Categoría *", weight="bold", size="2", color=color_texto_secundario),
                                rx.select(
                                    ["Creacionales", "Estructurales", "De Comportamiento"],
                                    value=EditPatternState.edit_categoria,
                                    on_change=EditPatternState.set_edit_categoria,
                                    width="100%"
                                ),
                                width="100%"
                            ),
                            columns="2", spacing="5", width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text("Descripción Breve *", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(value=EditPatternState.edit_descripcion, on_change=EditPatternState.set_edit_descripcion, width="100%", height="100px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Diagrama UML (Imagen)", weight="bold", size="2", color=color_texto_secundario),
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Imagen Actual:", size="1", color=color_texto_gris),
                                    rx.image(src=EditPatternState.diagrama_actual, height="120px", border_radius="8px", border=f"1px solid {color_borde}", object_fit="contain"),
                                    
                                    rx.cond(
                                        EditPatternState.diagrama_actual != "/placeholder.png",
                                        rx.button(
                                            rx.icon("trash-2", size=14), "Borrar imagen",
                                            on_click=EditPatternState.eliminar_imagen_actual,
                                            size="1", color_scheme="red", variant="ghost", cursor="pointer", margin_top="0.5em"
                                        )
                                    ),
                                    align="center"
                                ),
                                rx.upload(
                                    rx.vstack(
                                        rx.button("Reemplazar imagen", color_scheme="indigo", variant="outline"),
                                        rx.text("Arrastra aquí solo si quieres cambiarla.", color=color_texto_gris, size="1"),
                                        align="center", justify="center", padding="2em", border=f"2px dashed {color_borde_input}", border_radius="8px", background_color=color_fondo_pagina, width="100%", cursor="pointer"
                                    ),
                                    id="upload_diagrama_edit", 
                                    multiple=False, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, max_files=1
                                ),
                                width="100%", spacing="5"
                            ),
                            
                            rx.cond(
                                rx.selected_files("upload_diagrama_edit").length() > 0,
                                rx.hstack(
                                    rx.icon("image", color=color_exito, size=18),
                                    rx.text("Nueva imagen lista: ", weight="bold", size="2", color=color_exito_oscuro),
                                    rx.foreach(rx.selected_files("upload_diagrama_edit"), lambda file: rx.text(file, size="2", color=color_exito_check)),
                                    rx.spacer(),
                                    rx.button(rx.icon("trash-2", size=16), on_click=rx.clear_selected_files("upload_diagrama_edit"), variant="ghost", color_scheme="red", size="1", cursor="pointer"),
                                    align="center", width="100%", padding="0.75em 1em", background_color=color_exito_fondo_claro, border_radius="6px", border="1px solid #bbf7d0"
                                )
                            ),
                            width="100%", margin_top="1em"
                        ),
                        
                        rx.divider(margin_y="2em"),
                        rx.heading("Detalles Teóricos", size="5", weight="bold", color=color_texto_principal),
                        
                        rx.grid(
                            rx.vstack(
                                rx.text("Ventajas", weight="bold", size="2", color=color_texto_secundario),
                                rx.text_area(value=EditPatternState.edit_ventajas, on_change=EditPatternState.set_edit_ventajas, width="100%", height="150px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            rx.vstack(
                                rx.text("Desventajas", weight="bold", size="2", color=color_texto_secundario),
                                rx.text_area(value=EditPatternState.edit_desventajas, on_change=EditPatternState.set_edit_desventajas, width="100%", height="150px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                                width="100%"
                            ),
                            columns="2", spacing="5", width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Ejemplos de Uso", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(value=EditPatternState.edit_ejemplos, on_change=EditPatternState.set_edit_ejemplos, width="100%", height="100px", border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),

                        rx.vstack(
                            rx.text("Pseudocódigo", weight="bold", size="2", color=color_texto_secundario),
                            rx.text_area(value=EditPatternState.edit_pseudocodigo, on_change=EditPatternState.set_edit_pseudocodigo, width="100%", height="200px", style={"font_family": "monospace"}, border=f"1px solid {color_borde_input}", background_color="white", color=color_texto_principal),
                            width="100%", margin_top="1em"
                        ),
                        
                        rx.cond(
                            EditPatternState.error_edicion != "",
                            rx.text(EditPatternState.error_edicion, color=color_error, size="2", weight="medium", margin_top="1em")
                        ),

                        rx.button(
                            "Guardar Cambios", 
                            on_click=EditPatternState.guardar_cambios(rx.upload_files(upload_id="upload_diagrama_edit")),
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