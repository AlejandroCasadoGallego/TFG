
import reflex as rx
from ..state.auth_state import AuthState
from ..colores import *

def landing_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Bienvenido a PatternLab", size="9", color=color_texto_principal, margin_bottom="0.2em", weight="bold"),
            rx.text("La plataforma educativa para dominar patrones de diseño.", size="5", color=color_texto_secundario, text_align="center"),
            
            rx.hstack(
                rx.link(rx.button("Iniciar Sesión", size="4", color_scheme="indigo", cursor="pointer"), href="/login"),
                rx.link(rx.button("Registrarse", size="4", variant="outline", color_scheme="indigo", cursor="pointer"), href="/register"),
                spacing="4", margin_top="2.5em"
            ),
            
            rx.link(
                rx.button(
                    rx.hstack(rx.icon("library", size=18), rx.text("Explorar Biblioteca Abierta"), align="center", spacing="2"),
                    variant="surface", 
                    size="3", 
                    color_scheme="gray", 
                    color=color_texto_secundario,
                    margin_top="2em", 
                    cursor="pointer",
                    box_shadow="sm"
                ),
                href="/biblioteca",
                underline="none"
            ),
            
            align="center", padding="2em",
        ),
        height="100vh", background=f"linear-gradient(135deg, #f5f7ff 0%, {color_fondo_blanco} 100%)"
    )

def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.icon("graduation-cap", size=48, color="white"),
                    background_color=color_primario, padding="1.5em", border_radius="50%", margin_bottom="1em", box_shadow="lg"
                ),
                rx.heading("Acceso", size="7", weight="bold", color=color_texto_principal),
                rx.text("Plataforma de Patrones de Diseño", color=color_texto_gris, margin_bottom="2em"),
                rx.vstack(
                    rx.text("Correo Electrónico", size="2", weight="bold", color=color_texto_secundario, width="100%"),
                    rx.input(placeholder="admin@test.com", on_change=AuthState.set_correo_input, on_key_down=AuthState.handle_key_login, size="3", width="100%", variant="soft", color=color_negro, background_color=color_fondo_claro),
                    spacing="2", width="100%"
                ),
                rx.vstack(
                    rx.text("Contraseña", size="2", weight="bold", color=color_texto_secundario, width="100%"),
                    rx.input(type="password", placeholder="••••••••", on_change=AuthState.set_pass_input, on_key_down=AuthState.handle_key_login, size="3", width="100%", variant="soft", color=color_negro, background_color=color_fondo_claro),
                    spacing="2", width="100%", margin_top="1em"
                ),
                rx.cond(
                    AuthState.error_mensaje != "",
                    rx.callout(AuthState.error_mensaje, icon="triangle-alert", color_scheme="red", variant="surface", width="100%", margin_top="1em"),
                ),
                rx.button("Entrar", on_click=AuthState.iniciar_sesion, size="4", width="100%", margin_top="2em", cursor="pointer", background_color=color_primario, color="white"),
                padding="2em", align="center", width="100%"
            ),
            size="4", max_width="400px", background_color="white", border=f"1px solid {color_borde}", box_shadow="xl"
        ),
        height="100vh", background_color=color_fondo_claro
    )

def register_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Registro de Estudiante", size="7", color=color_texto_principal, weight="bold"),
                rx.text("Crea tu cuenta para empezar a aprender", color=color_texto_gris, size="2", margin_bottom="1.5em"),
                
                rx.vstack(
                    rx.input(placeholder="Nombre Completo", on_change=AuthState.set_nombre_input, on_key_down=AuthState.handle_key_registro, width="100%", color=color_texto_principal, variant="surface"),
                    rx.input(placeholder="Correo Electrónico", on_change=AuthState.set_correo_input, on_key_down=AuthState.handle_key_registro, width="100%", color=color_texto_principal, variant="surface"),
                    rx.input(type="password", placeholder="Contraseña", on_change=AuthState.set_pass_input, on_key_down=AuthState.handle_key_registro, width="100%", color=color_texto_principal, variant="surface"),
                    rx.text("Mín. 8 caracteres, mayúsculas, minúsculas, números y un símbolo.", size="1", color=color_texto_claro),
                    spacing="3", width="100%"
                ),

                rx.cond(
                    AuthState.error_mensaje != "",
                    rx.text(AuthState.error_mensaje, color=color_error, size="2", weight="medium")
                ),
                
                rx.button("Crear Cuenta", on_click=AuthState.registrar_usuario, width="100%", color_scheme="indigo", margin_top="1em", cursor="pointer"),
                rx.link("¿Ya tienes cuenta? Inicia sesión", href="/login", size="2", color=color_primario, margin_top="1em"),
                align="center", width="100%"
            ),
            padding="2.5em", width="400px", background_color="white", box_shadow="xl"
        ),
        height="100vh", background_color=color_fondo_claro
    )

def primer_acceso_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.icon("shield-alert", size=48, color=color_advertencia), 
                    background_color=color_amarillo_fondo, padding="1em", border_radius="50%", margin_bottom="1em"
                ),
                rx.heading("Acción Requerida", size="7", weight="bold", color=color_texto_principal, text_align="center"),
                rx.text("Por motivos de seguridad, debes cambiar la contraseña temporal proporcionada por el administrador antes de acceder a tu cuenta.", color=color_texto_terciario, text_align="center", margin_bottom="1.5em"),
                
                rx.vstack(
                    rx.text("Nueva Contraseña", weight="bold", size="2", color=color_texto_secundario, width="100%"),
                    rx.input(type="password", placeholder="••••••••", value=AuthState.pass_forzado_1, on_change=AuthState.set_pass_forzado_1, on_key_down=AuthState.handle_key_forzado, width="100%", background_color="white", color=color_texto_principal, border=f"1px solid {color_borde_input}"),
                    
                    rx.text("Repite la Contraseña", weight="bold", size="2", color=color_texto_secundario, width="100%", margin_top="0.5em"),
                    rx.input(type="password", placeholder="••••••••", value=AuthState.pass_forzado_2, on_change=AuthState.set_pass_forzado_2, on_key_down=AuthState.handle_key_forzado, width="100%", background_color="white", color=color_texto_principal, border=f"1px solid {color_borde_input}"),
                    rx.text("Mín. 8 caracteres, mayúsculas, minúsculas, números y un símbolo.", size="1", color=color_texto_claro),
                    spacing="2", width="100%"
                ),

                rx.cond(AuthState.error_pass_forzado != "", rx.text(AuthState.error_pass_forzado, color=color_error, size="2", weight="medium", margin_top="1em")),
                
                rx.vstack(
                    rx.button("Actualizar y Entrar", on_click=AuthState.guardar_pass_forzado, color_scheme="indigo", width="100%", cursor="pointer"),
                    rx.button("Cerrar Sesión", on_click=AuthState.cerrar_sesion, variant="ghost", color_scheme="gray", width="100%", cursor="pointer"),
                    spacing="3", width="100%", margin_top="2em"
                ),
                padding="2em", align="center", width="100%"
            ),
            width="450px", background_color="white", box_shadow="xl", border=f"1px solid {color_borde}"
        ),
        height="100vh", background_color=color_fondo_claro
    )