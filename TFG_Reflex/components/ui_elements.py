import reflex as rx
from ..colores import *

def stat_card(titulo: str, valor: str, icono: str, color_bg: str, ruta: str = None) -> rx.Component:
    tarjeta = rx.card(
        rx.hstack(
            rx.center(
                rx.icon(icono, size=28, color="white"),
                background_color=color_bg,
                border_radius="12px",
                width="60px",
                height="60px",
                box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
            ),
            rx.vstack(
                rx.text(titulo, size="2", weight="bold", color=color_texto_terciario),
                rx.text(valor, size="7", weight="bold", color=color_texto_principal),
                spacing="1",
                align_items="start"
            ),
            align="center",
            spacing="4"
        ),
        size="3",
        width="100%",
        background_color="white",
        border=f"1px solid {color_borde}",
        _hover={
            "box_shadow": "lg", 
            "transform": "translateY(-2px)", 
            "transition": "all 0.2s ease-in-out",
            "border_color": color_bg
        } if ruta else {}
    )

    if ruta:
        return rx.link(tarjeta, href=ruta, underline="none", width="100%")
    
    return tarjeta

def sidebar_item(texto: str, icon: str, ruta: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color=color_texto_terciario),
            rx.text(texto, size="3", weight="medium", color=color_texto_secundario),
            spacing="3",
            padding="12px 16px",
            border_radius="8px",
            _hover={
                "background_color": "#e0e7ff",
                "color": color_primario_oscuro,
            },
            width="100%",
            align="center"
        ),
        href=ruta,
        underline="none",
        width="100%"
    )