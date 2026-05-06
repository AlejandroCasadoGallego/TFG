import reflex as rx
from ..state.base_state import BaseState
from ..state.patterns_state import PatternsState
from ..components.layout import sidebar_layout, header_component, public_header
from ..colores import *

def badge_categoria(categoria: str) -> rx.Component:
    color = rx.match(
        categoria,
        ("Creacionales", "green"),
        ("Estructurales", "blue"),
        ("De Comportamiento", "orange"),
        "gray"
    )
    return rx.badge(categoria, color_scheme=color, variant="solid")

def render_imagen_fallback(patron: dict, alto: str) -> rx.Component:
    return rx.cond(
        patron["diagrama"] != "/placeholder.png",
        rx.image(src=patron["diagrama"], height=alto, width="100%", object_fit="contain"),
        rx.center(
            rx.icon("layout-template", size=40, color=color_gris_medio),
            width="100%", height=alto, background_color=color_fondo_hover
        )
    )

def patron_card_grid(patron: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            render_imagen_fallback(patron, "150px"),
            
            rx.vstack(
                rx.hstack(
                    badge_categoria(patron["categoria"]),
                    rx.cond(
                        (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                        rx.badge(rx.cond(patron["activo"], "Activo", "Inactivo"), color_scheme=rx.cond(patron["activo"], "green", "red"), variant="solid")
                    ),
                    justify="between", width="100%", flex_wrap="wrap"
                ),
                rx.heading(patron["nombre"], size="5", weight="bold", color=color_texto_principal, margin_top="0.5em"),
                
                rx.box(
                    rx.text(patron["descripcion"], color=color_texto_terciario, size="2", style={"display": "-webkit-box", "-webkit-line-clamp": "3", "-webkit-box-orient": "vertical", "overflow": "hidden"}),
                    flex="1", width="100%", margin_bottom="0.5em"
                ),
                
                rx.divider(width="100%", margin_bottom="0.5em"),
                
                rx.hstack(
                    rx.button(
                        rx.icon("book-open", size=16), "Ver Patrón", 
                        on_click=rx.redirect(f"/patron/{patron['id']}"), 
                        background_color=color_primario, color="white", _hover={"background_color": color_primario_oscuro},
                        flex="1", cursor="pointer"
                    ),
                    rx.cond(
                        (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                        rx.button(
                            rx.icon(rx.cond(patron["activo"], "eye-off", "eye"), size=16),
                            rx.cond(patron["activo"], "Desactivar", "Activar"),
                            on_click=lambda: PatternsState.toggle_estado_patron(patron["id"]), 
                            color_scheme=rx.cond(patron["activo"], "red", "green"), 
                            variant="solid", flex="1", cursor="pointer"
                        )
                    ),
                    width="100%", spacing="2"
                ),
                padding="1.5em", align_items="start", width="100%", height="100%", flex="1"
            ),
            spacing="0", height="100%"
        ),
        padding="0", width="100%", height="100%", border=f"1px solid {color_borde}", overflow="hidden",
        opacity=rx.cond(patron["activo"], "1", "0.65"), 
        _hover={"box_shadow": "md", "transform": "translateY(-2px)", "transition": "all 0.2s"}
    )

def patron_card_list(patron: dict) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.box(
                render_imagen_fallback(patron, "100px"),
                width="120px", flex_shrink="0", overflow="hidden", border_radius="6px", border=f"1px solid {color_borde}"
            ),
            
            rx.vstack(
                rx.hstack(
                    rx.heading(patron["nombre"], size="4", weight="bold", color=color_texto_principal), 
                    badge_categoria(patron["categoria"]), 
                    rx.cond(
                        (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                        rx.badge(rx.cond(patron["activo"], "Activo", "Inactivo"), color_scheme=rx.cond(patron["activo"], "green", "red"), variant="soft")
                    ),
                    align="center", spacing="2", flex_wrap="wrap"
                ),
                rx.text(patron["descripcion"], color=color_texto_terciario, size="2", margin_top="0.2em"),
                align_items="start", justify="center", width="100%", padding_x="1em"
            ),
            
            rx.spacer(),
            
            rx.flex(
                rx.button(rx.icon("book-open", size=16),"Ver Patrón", on_click=rx.redirect(f"/patron/{patron['id']}"), color_scheme="indigo", variant="soft", flex="1", cursor="pointer"),
                rx.cond(
                    (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                    rx.button(
                        rx.icon(rx.cond(patron["activo"], "eye-off", "eye"), size=16),
                        rx.cond(patron["activo"], "Desactivar", "Activar"),
                        on_click=lambda: PatternsState.toggle_estado_patron(patron["id"]), 
                        color_scheme=rx.cond(patron["activo"], "red", "green"), 
                        variant="solid", width="100%", cursor="pointer"
                    )
                ),
                direction="column", spacing="2", width="160px", flex_shrink="0", justify="center"
            ),
            align="center", width="100%", direction={"initial": "column", "md": "row"}, gap="4"
        ),
        padding="1.2em", width="100%", border=f"1px solid {color_borde}", 
        opacity=rx.cond(patron["activo"], "1", "0.65"),
        _hover={"background_color": color_fondo_hover, "box_shadow": "sm"}
    )


def contenido_biblioteca() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.vstack(
                rx.heading("Biblioteca de Patrones", size="8", weight="bold", color=color_texto_principal),
                rx.text("Explora y domina los patrones de diseño del Gang of Four.", color=color_texto_gris, size="3"),
                align_items="start"
            ),
            rx.spacer(),

            rx.cond(
                (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                rx.button(
                    rx.icon("plus", size=18), "Crear Patrón",
                    on_click=rx.redirect("/crear-patron"),
                    color_scheme="indigo", cursor="pointer", margin_right="1em"
                )
            ),

            rx.input(
                rx.input.slot(rx.icon("search", size=18, color=color_texto_gris)), 
                placeholder="Buscar por nombre...", 
                value=PatternsState.busqueda, 
                on_change=PatternsState.set_busqueda, 
                width="100%", 
                max_width="350px", 
                size="3", 
                radius="full", 
                background_color="white", 
                border=f"1px solid {color_borde_input}",
                color=color_texto_principal
            ),
            width="100%", align="end", margin_bottom="2em", flex_direction=["column", "column", "row"], gap="4"
        ),
        
        rx.hstack(
            rx.hstack(
                rx.foreach(
                    ["Todas", "Creacionales", "Estructurales", "De Comportamiento"],
                    lambda cat: rx.button(cat, on_click=lambda: PatternsState.set_categoria(cat), variant=rx.cond(PatternsState.categoria_seleccionada == cat, "solid", "surface"), color_scheme="indigo", radius="full", cursor="pointer")
                ),
                spacing="2"
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.icon("layout-grid", size=18), "Cuadrícula",
                    on_click=lambda: PatternsState.set_modo_vista("grid"), 
                    variant=rx.cond(PatternsState.modo_vista == "grid", "solid", "soft"), 
                    color_scheme="indigo", cursor="pointer"
                ),
                rx.button(
                    rx.icon("list", size=18), "Lista",
                    on_click=lambda: PatternsState.set_modo_vista("list"), 
                    variant=rx.cond(PatternsState.modo_vista == "list", "solid", "soft"), 
                    color_scheme="indigo", cursor="pointer"
                ),
                spacing="2"
            ),
            width="100%", margin_bottom="2em", align="center"
        ),

        rx.cond(
            PatternsState.patrones_filtrados.length() > 0,
            rx.cond(
                PatternsState.modo_vista == "grid",
                rx.grid(rx.foreach(PatternsState.patrones_filtrados, patron_card_grid), columns={"initial": "1", "sm": "2", "md": "3", "lg": "4"}, spacing="5", width="100%"),
                rx.vstack(rx.foreach(PatternsState.patrones_filtrados, patron_card_list), spacing="3", width="100%")
            ),
            rx.center(
                rx.vstack(
                    rx.icon("search-x", size=48, color=color_texto_claro),
                    rx.heading("No se encontraron patrones", size="5", color=color_texto_principal),
                    rx.text("Prueba con otra búsqueda o selecciona una categoría diferente.", color=color_texto_gris),
                    align="center", spacing="3"
                ),
                padding="4em", width="100%", border=f"2px dashed {color_borde}", border_radius="12px", background_color="white"
            )
        ),
        width="100%", max_width="1400px", margin="0 auto"
    )


def biblioteca_page() -> rx.Component:
    return rx.cond(
        BaseState.usuario_actual == "",
        rx.vstack(
            public_header(),
            rx.box(contenido_biblioteca(), padding="3em", width="100%"),
            width="100%", min_height="100vh", background_color=color_fondo_pagina
        ),
        rx.flex(
            sidebar_layout(),
            rx.box(
                rx.vstack(
                    header_component(titulo=""),
                    contenido_biblioteca(), 
                    padding="3em", 
                    width="100%"
                ), 
                flex="1", height="100vh", background_color=color_fondo_pagina, overflow="auto"
            ),
            width="100%"
        )
    )