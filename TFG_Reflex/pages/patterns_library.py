import reflex as rx
from ..state.base_state import BaseState
from ..state.patterns_state import PatternsState
from ..components.layout import sidebar_layout, header_component, public_header

# --- DISEÑO DE LAS TARJETAS (GRID VS LISTA) ---

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
    """Renderiza la imagen real, o un icono elegante de 'plano' si no existe."""
    return rx.cond(
        patron["diagrama"] != "/placeholder.png",
        rx.image(src=patron["diagrama"], height=alto, width="100%", object_fit="contain"),
        rx.center(
            rx.icon("layout-template", size=40, color="#94a3b8"), # Icono gris azulado
            width="100%", height=alto, background_color="#f1f5f9"
        )
    )

def patron_card_grid(patron: dict) -> rx.Component:
    """Formato Cuadrícula: Imagen grande arriba, info debajo."""
    return rx.card(
        rx.vstack(
            # Imagen/Diagrama con el nuevo fallback
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
                rx.heading(patron["nombre"], size="5", weight="bold", color="#111827", margin_top="0.5em"),
                
                rx.box(
                    rx.text(patron["descripcion"], color="#4b5563", size="2", style={"display": "-webkit-box", "-webkit-line-clamp": "3", "-webkit-box-orient": "vertical", "overflow": "hidden"}),
                    flex="1", width="100%", margin_bottom="0.5em"
                ),
                
                rx.divider(width="100%", margin_bottom="0.5em"),
                
                # Botonera con ICONOS
                rx.hstack(
                    rx.button(
                        rx.icon("book-open", size=16), "Ver Patrón", 
                        on_click=rx.redirect(f"/patron/{patron['id']}"), 
                        background_color="#4f46e5", color="white", _hover={"background_color": "#4338ca"}, # Colores CSS directos e infalibles
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
        padding="0", width="100%", height="100%", border="1px solid #e5e7eb", overflow="hidden",
        # Hacemos que toda la tarjeta se vuelva semitransparente si está inactiva
        opacity=rx.cond(patron["activo"], "1", "0.65"), 
        _hover={"box_shadow": "md", "transform": "translateY(-2px)", "transition": "all 0.2s"}
    )

def patron_card_list(patron: dict) -> rx.Component:
    """Formato Lista: Horizontal estructurado en 3 columnas rígidas."""
    return rx.card(
        rx.flex(
            # Columna 1: Imagen cuadrada rígida
            rx.box(
                render_imagen_fallback(patron, "100px"),
                width="120px", flex_shrink="0", overflow="hidden", border_radius="6px", border="1px solid #e5e7eb"
            ),
            
            # Columna 2: Textos (Ocupa el espacio restante)
            rx.vstack(
                rx.hstack(
                    rx.heading(patron["nombre"], size="4", weight="bold", color="#111827"), 
                    badge_categoria(patron["categoria"]), 
                    rx.cond(
                        (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                        rx.badge(rx.cond(patron["activo"], "Activo", "Inactivo"), color_scheme=rx.cond(patron["activo"], "green", "red"), variant="soft")
                    ),
                    align="center", spacing="2", flex_wrap="wrap"
                ),
                rx.text(patron["descripcion"], color="#4b5563", size="2", margin_top="0.2em"),
                align_items="start", justify="center", width="100%", padding_x="1em"
            ),
            
            rx.spacer(),
            
            # Columna 3: Botonera alineada a la derecha
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
        padding="1.2em", width="100%", border="1px solid #e5e7eb", 
        opacity=rx.cond(patron["activo"], "1", "0.65"), # Efecto visual de inactivo
        _hover={"background_color": "#f8fafc", "box_shadow": "sm"}
    )

# --- CONTENIDO PRINCIPAL ---

def contenido_biblioteca() -> rx.Component:
    return rx.vstack(
        # 1. Cabecera y Buscador (CORREGIDO)
        rx.flex(
            rx.vstack(
                rx.heading("Biblioteca de Patrones", size="8", weight="bold", color="#111827"),
                rx.text("Explora y domina los patrones de diseño del Gang of Four.", color="#6b7280", size="3"),
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

            # LA LUPA Y EL BUSCADOR AHORA SON VISIBLES
            rx.input(
                rx.input.slot(rx.icon("search", size=18, color="#6b7280")), # Lupa interior
                placeholder="Buscar por nombre...", 
                value=PatternsState.busqueda, 
                on_change=PatternsState.set_busqueda, 
                width="100%", 
                max_width="350px", 
                size="3", 
                radius="full", 
                background_color="white", 
                border="1px solid #d1d5db", # Borde gris para que se vea
                color="#111827"
            ),
            width="100%", align="end", margin_bottom="2em", flex_direction=["column", "column", "row"], gap="4"
        ),
        
        # 2. Controles (Categorías y Vista)
        rx.hstack(
            rx.hstack(
                rx.foreach(
                    ["Todas", "Creacionales", "Estructurales", "De Comportamiento"],
                    lambda cat: rx.button(cat, on_click=lambda: PatternsState.set_categoria(cat), variant=rx.cond(PatternsState.categoria_seleccionada == cat, "solid", "surface"), color_scheme="indigo", radius="full", cursor="pointer")
                ),
                spacing="2"
            ),
            rx.spacer(),
            # BOTONES DE VISTA CORREGIDOS (A prueba de fallos con texto)
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

        # 3. Catálogo o Empty State
        rx.cond(
            PatternsState.patrones_filtrados.length() > 0,
            rx.cond(
                PatternsState.modo_vista == "grid",
                rx.grid(rx.foreach(PatternsState.patrones_filtrados, patron_card_grid), columns={"initial": "1", "sm": "2", "md": "3", "lg": "4"}, spacing="5", width="100%"),
                rx.vstack(rx.foreach(PatternsState.patrones_filtrados, patron_card_list), spacing="3", width="100%")
            ),
            rx.center(
                rx.vstack(
                    rx.icon("search-x", size=48, color="#9ca3af"),
                    rx.heading("No se encontraron patrones", size="5", color="#111827"),
                    rx.text("Prueba con otra búsqueda o selecciona una categoría diferente.", color="#6b7280"),
                    align="center", spacing="3"
                ),
                padding="4em", width="100%", border="2px dashed #e5e7eb", border_radius="12px", background_color="white"
            )
        ),
        width="100%", max_width="1400px", margin="0 auto"
    )

# --- WRAPPER ---

def biblioteca_page() -> rx.Component:
    return rx.cond(
        BaseState.usuario_actual == "",
        # SI ES VISITANTE
        rx.vstack(
            public_header(),
            rx.box(contenido_biblioteca(), padding="3em", width="100%"),
            width="100%", min_height="100vh", background_color="#f9fafb"
        ),
        # SI ESTÁ LOGUEADO
        rx.flex(
            sidebar_layout(),
            rx.box(
                rx.vstack(
                    header_component(titulo=""), # <--- ¡AQUÍ ESTÁ EL TRUCO!
                    contenido_biblioteca(), 
                    padding="3em", 
                    width="100%"
                ), 
                flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
            ),
            width="100%"
        )
    )