# pages/pattern_detail.py
import reflex as rx
from ..state.base_state import BaseState
from ..state.pattern_detail_state import PatternDetailState
from ..components.layout import sidebar_layout, header_component, public_header

# --- COMPONENTES AUXILIARES ---

def badge_categoria_detalle(categoria: str) -> rx.Component:
    color = rx.match(categoria, ("Creacionales", "green"), ("Estructurales", "blue"), ("De Comportamiento", "orange"), "gray")
    return rx.badge(categoria, color_scheme=color, variant="soft", size="2")

def miniatura_clicable(ruta_imagen: str) -> rx.Component:
    """Crea una miniatura que, al clicar, abre la imagen en grande (Lightbox)."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.box(
                rx.image(src=ruta_imagen, width="120px", height="120px", object_fit="contain", border_radius="8px", border="1px solid #e5e7eb", background_color="#f8fafc"),
                rx.center(
                    rx.icon("zoom-in", color="white", size=24),
                    position="absolute", top="0", left="0", width="100%", height="100%", background_color="rgba(0,0,0,0.4)", border_radius="8px", opacity="0", _hover={"opacity": "1"}, transition="opacity 0.2s"
                ),
                position="relative", cursor="pointer", box_shadow="sm", _hover={"box_shadow": "md", "transform": "scale(1.02)"}, transition="all 0.2s"
            )
        ),
        rx.dialog.content(
            rx.dialog.close(rx.button(rx.icon("x", size=20), variant="ghost", color_scheme="gray", position="absolute", top="1em", right="1em", cursor="pointer")),
            rx.center(rx.image(src=ruta_imagen, max_width="100%", max_height="80vh", object_fit="contain", border_radius="8px")),
            max_width="80vw", background_color="transparent", box_shadow="none" 
        )
    )

def panel_teoria() -> rx.Component:
    return rx.vstack(
        rx.heading("Concepto Principal", size="5", color="#111827", margin_bottom="0.5em"),
        rx.text(PatternDetailState.patron_actual["descripcion"], color="#374151", size="3", line_height="1.6"),
        width="100%", padding="2em", background_color="white", border="1px solid #e5e7eb", border_radius="8px", border_top_left_radius="0"
    )

def panel_analisis() -> rx.Component:
    return rx.grid(
        # Condición: Solo muestra la tarjeta de Ventajas si hay texto
        rx.cond(
            PatternDetailState.patron_actual["ventajas"] != "",
            rx.card(
                rx.vstack(rx.hstack(rx.icon("check-circle-2", color="#16a34a"), rx.heading("Ventajas", size="4", color="#166534")), rx.divider(), rx.text(PatternDetailState.patron_actual["ventajas"], color="#374151", white_space="pre-wrap")),
                background_color="#f0fdf4", border="1px solid #bbf7d0", width="100%"
            )
        ),
        # Condición: Solo muestra la tarjeta de Desventajas si hay texto
        rx.cond(
            PatternDetailState.patron_actual["desventajas"] != "",
            rx.card(
                rx.vstack(rx.hstack(rx.icon("x-circle", color="#dc2626"), rx.heading("Desventajas", size="4", color="#991b1b")), rx.divider(), rx.text(PatternDetailState.patron_actual["desventajas"], color="#374151", white_space="pre-wrap")),
                background_color="#fef2f2", border="1px solid #fecaca", width="100%"
            )
        ),
        columns="2", spacing="5", width="100%", padding="2em", background_color="white", border="1px solid #e5e7eb", border_radius="8px", border_top_left_radius="0"
    )

def panel_implementacion() -> rx.Component:
    return rx.vstack(
        # Condición: Mostrar ejemplos solo si existen
        rx.cond(
            PatternDetailState.patron_actual["ejemplos"] != "",
            rx.vstack(
                rx.heading("Ejemplo de Uso", size="5", color="#111827"),
                rx.text(PatternDetailState.patron_actual["ejemplos"], color="#374151", margin_bottom="2em", white_space="pre-wrap"),
                width="100%", align_items="start"
            )
        ),
        # Condición: Mostrar pseudocódigo solo si existe
        rx.cond(
            PatternDetailState.patron_actual["pseudocodigo"] != "",
            rx.vstack(
                rx.heading("Pseudocódigo Estructural", size="5", color="#111827"),
                rx.box(
                    rx.text(
                        PatternDetailState.patron_actual["pseudocodigo"],
                        font_family="'Courier New', Courier, monospace",
                        color="#f8fafc",
                        size="3",
                        white_space="pre", 
                        line_height="1.6"
                    ),
                    width="100%", background_color="#1e293b", padding="1.5em", border_radius="8px", 
                    overflow_x="auto", margin_top="0.5em", box_shadow="inset 0 2px 4px 0 rgb(0 0 0 / 0.05)", border="1px solid #0f172a"
                ),
                width="100%", align_items="start"
            )
        ),
        width="100%", padding="2em", background_color="white", border="1px solid #e5e7eb", border_radius="8px", border_top_left_radius="0"
    )

# --- VISTA PRINCIPAL ---

def contenido_detalle() -> rx.Component:
    return rx.cond(
        PatternDetailState.error_carga,
        rx.center(rx.vstack(rx.icon("file-warning", size=48, color="#ef4444"), rx.heading("Patrón no encontrado o inactivo", size="6"), rx.button("Volver", on_click=rx.redirect("/biblioteca"), cursor="pointer"))),
        rx.vstack(
            rx.button(rx.icon("arrow-left", size=16), "Volver a la Biblioteca", color="#4b5563", on_click=rx.redirect("/biblioteca"), variant="ghost", color_scheme="gray", cursor="pointer", margin_bottom="1em"),
            
            rx.hstack(
                rx.hstack(
                    # Condición: Mostrar miniatura SOLO si hay diagrama y no es el placeholder
                    rx.cond(
                        (PatternDetailState.patron_actual["diagrama"] != "") & (PatternDetailState.patron_actual["diagrama"] != "/placeholder.png"),
                        miniatura_clicable(PatternDetailState.patron_actual["diagrama"])
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.heading(PatternDetailState.patron_actual["nombre"], size="8", weight="bold", color="#111827"),
                            rx.cond((BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"), rx.badge(rx.cond(PatternDetailState.patron_actual["activo"], "Activo", "Inactivo"), color_scheme=rx.cond(PatternDetailState.patron_actual["activo"], "green", "red"), variant="solid")),
                            align="center", spacing="3"
                        ),
                        badge_categoria_detalle(PatternDetailState.patron_actual["categoria"]),
                        align_items="start", justify="center"
                    ),
                    spacing="5", align="center"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(rx.icon("download", size=18), "Descargar PDF", on_click=PatternDetailState.descargar_pdf, color_scheme="gray", variant="surface", cursor="pointer"),
                    rx.cond(
                        (BaseState.usuario_rol == "admin") | (BaseState.usuario_rol == "docente"),
                        rx.hstack(
                            rx.button(rx.icon("pencil", size=18), "Modificar", on_click=rx.redirect(f"/editar-patron/{PatternDetailState.patron_actual['id']}"), color_scheme="indigo", variant="solid", cursor="pointer"),
                            rx.button(rx.icon(rx.cond(PatternDetailState.patron_actual["activo"], "eye-off", "eye"), size=18), rx.cond(PatternDetailState.patron_actual["activo"], "Desactivar", "Activar"), on_click=PatternDetailState.toggle_estado_actual, color_scheme=rx.cond(PatternDetailState.patron_actual["activo"], "red", "green"), cursor="pointer"),
                            spacing="3"
                        )
                    ),
                    spacing="3"
                ),
                width="100%", align="center", margin_bottom="2em", flex_wrap="wrap", gap="4"
            ),
            
            # 3. PESTAÑAS (TABS) DINÁMICAS
            rx.tabs.root(
                rx.tabs.list(
                    # La pestaña de concepto SIEMPRE se muestra (es obligatoria)
                    rx.tabs.trigger(
                        rx.hstack(rx.icon("book-text", size=18, color="#374151"), rx.text("Concepto y Teoría", color="#374151", weight="bold")), 
                        value="concepto", cursor="pointer"
                    ),
                    
                    # Condición Pestaña 2: Mostrar si Ventajas O Desventajas no están vacíos
                    rx.cond(
                        (PatternDetailState.patron_actual["ventajas"] != "") | (PatternDetailState.patron_actual["desventajas"] != ""),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("scale", size=18, color="#374151"), rx.text("Pros y Contras", color="#374151", weight="bold")), 
                            value="analisis", cursor="pointer"
                        )
                    ),
                    
                    # Condición Pestaña 3: Mostrar si Ejemplos O Pseudocódigo no están vacíos
                    rx.cond(
                        (PatternDetailState.patron_actual["ejemplos"] != "") | (PatternDetailState.patron_actual["pseudocodigo"] != ""),
                        rx.tabs.trigger(
                            rx.hstack(rx.icon("code", size=18, color="#374151"), rx.text("Implementación", color="#374151", weight="bold")), 
                            value="implementacion", cursor="pointer"
                        )
                    ),
                    size="2"
                ),
                
                # CONTENIDOS DE LAS PESTAÑAS
                rx.tabs.content(panel_teoria(), value="concepto"),
                
                rx.cond(
                    (PatternDetailState.patron_actual["ventajas"] != "") | (PatternDetailState.patron_actual["desventajas"] != ""),
                    rx.tabs.content(panel_analisis(), value="analisis")
                ),
                
                rx.cond(
                    (PatternDetailState.patron_actual["ejemplos"] != "") | (PatternDetailState.patron_actual["pseudocodigo"] != ""),
                    rx.tabs.content(panel_implementacion(), value="implementacion")
                ),
                
                default_value="concepto", 
                width="100%",
                color_scheme="indigo"
            ),
            width="100%", max_width="1200px", margin="0 auto"
        )
    )

def pattern_detail_page() -> rx.Component:
    return rx.cond(
        BaseState.usuario_actual == "",
        rx.vstack(public_header(), rx.box(contenido_detalle(), padding="3em", width="100%"), width="100%", min_height="100vh", background_color="#f9fafb"),
        rx.flex(sidebar_layout(), rx.box(rx.vstack(header_component(titulo=""), contenido_detalle(), padding="3em", width="100%"), flex="1", height="100vh", background_color="#f9fafb", overflow="auto"), width="100%")
    )