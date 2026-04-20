import reflex as rx
from ..state.grupo_state import GrupoState
from ..models.usuarios import Grupos
from ..components.layout import sidebar_layout, header_component

def modal_crear_grupo() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(rx.icon("folder-plus", size=18), "Nuevo Grupo", color_scheme="indigo", cursor="pointer")
        ),
        rx.dialog.content(
            rx.dialog.title("Crear Nuevo Grupo", color="#111827"),
            rx.dialog.description("Introduce un nombre para identificar al grupo. El código de acceso para que los estudiantes se unan se generará automáticamente.", size="2", color="#4b5563"),
            
            rx.vstack(
                rx.text("Nombre del Grupo *", weight="bold", size="2", color="#374151"),
                rx.input(
                    placeholder="Ej: Programación 1º DAW...",
                    on_change=GrupoState.set_nuevo_nombre,
                    value=GrupoState.nuevo_nombre,
                    width="100%",
                    border="1px solid #d1d5db", 
                    background_color="white", 
                    color="#111827"
                ),
                rx.cond(
                    GrupoState.error_creacion != "",
                    rx.text(GrupoState.error_creacion, color="#ef4444", size="2", weight="medium")
                ),
                spacing="3",
                width="100%",
                margin_top="1em"
            ),
            
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="surface", color_scheme="gray", color="#374151", on_click=GrupoState.limpiar_formulario, cursor="pointer")
                ),
                rx.dialog.close(
                    rx.button("Crear y Generar Código", on_click=GrupoState.crear_grupo, color_scheme="indigo", color="white", cursor="pointer")
                ),
                spacing="3",
                margin_top="2em",
                justify="end",
            ),
            max_width="450px",
            background_color="white"
        )
    )

def modal_enviar_codigo_global() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Invitar Estudiantes", color="#111827"),
            rx.dialog.description(f"Busca y selecciona a los alumnos para enviarles el código de '{GrupoState.grupo_sel_nombre}'.", size="2", color="#4b5563"),
            
            rx.vstack(
                rx.input(
                    rx.input.slot(rx.icon("search", size=16)),
                    placeholder="Buscar por nombre de usuario...",
                    on_change=GrupoState.set_busqueda_estudiante,
                    value=GrupoState.busqueda_estudiante,
                    width="100%",
                    border="1px solid #d1d5db", 
                    background_color="white", 
                    color="#111827"
                ),

                rx.scroll_area(
                    rx.vstack(
                        rx.foreach(GrupoState.estudiantes_filtrados, render_estudiante),
                        width="100%", spacing="0"
                    ),
                    height="220px", width="100%", border="1px solid #e5e7eb", border_radius="8px", background_color="#f9fafb"
                ),
                
                rx.hstack(
                    rx.text("Estudiantes seleccionados:", size="1", color="#6b7280"),
                    rx.badge(GrupoState.estudiantes_seleccionados.length(), color_scheme="indigo", radius="full"),
                    align="center"
                ),
                
                spacing="3",
                width="100%",
                margin_top="1em"
            ),
            
            rx.flex(
                rx.button("Cancelar", variant="surface", color_scheme="gray", color="#374151", on_click=GrupoState.cambiar_estado_modal(False), cursor="pointer"),
                rx.button("Enviar Notificaciones", on_click=GrupoState.enviar_codigo, color_scheme="indigo", color="white", cursor="pointer"),
                spacing="3",
                margin_top="2em",
                justify="end",
            ),
            max_width="450px",
            background_color="white"
        ),
        open=GrupoState.modal_envio_abierto,
        on_open_change=GrupoState.cambiar_estado_modal
    )

def modal_editar_grupo_global() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Grupo", color="#111827"),
            rx.dialog.description("Modifica los detalles, expulsa miembros o invita a nuevos alumnos.", size="2", color="#4b5563"),
            
            rx.scroll_area(
                rx.vstack(
                    
                    rx.text("Nombre del Grupo *", weight="bold", size="2", color="#374151", margin_top="1em"),
                    rx.input(
                        on_change=GrupoState.set_grupo_editar_nombre,
                        value=GrupoState.grupo_editar_nombre,
                        width="100%", border="1px solid #d1d5db"
                    ),
                    
                    rx.divider(margin_y="1em"),
                    
                    
                    rx.hstack(
                        rx.icon("users", size=16, color="#4b5563"),
                        rx.text("Miembros Actuales", weight="bold", size="2", color="#374151"),
                        align="center"
                    ),
                    rx.cond(
                        GrupoState.miembros_actuales.length() > 0,
                        rx.vstack(rx.foreach(GrupoState.miembros_actuales, render_miembro_actual), width="100%", spacing="0"),
                        rx.text("Aún no hay alumnos matriculados.", size="2", color="#9ca3af", font_style="italic")
                    ),
                    
                    rx.divider(margin_y="1em"),
                    
                    
                    rx.hstack(
                        rx.icon("user-plus", size=16, color="#4b5563"),
                        rx.text("Invitar a la clase", weight="bold", size="2", color="#374151"),
                        align="center"
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("search", size=14)),
                        placeholder="Buscar alumnos no matriculados...",
                        on_change=GrupoState.set_busqueda_invitar,
                        value=GrupoState.busqueda_invitar,
                        width="100%"
                    ),
                    rx.box(
                        rx.vstack(rx.foreach(GrupoState.candidatos_filtrados, render_candidato_invitar), width="100%", spacing="0"),
                        max_height="150px", overflow="auto", border="1px solid #e5e7eb", border_radius="8px", background_color="#f9fafb", margin_top="0.5em"
                    ),
                    
                    spacing="2", width="100%"
                ),
                height="400px", width="100%", padding_right="1em"
            ),
            
            rx.flex(
                rx.button("Cancelar", variant="surface", color_scheme="gray", on_click=GrupoState.cambiar_estado_editar(False), cursor="pointer"),
                rx.button("Guardar Cambios", on_click=GrupoState.guardar_edicion, color_scheme="indigo", cursor="pointer"),
                spacing="3", margin_top="1.5em", justify="end",
            ),
            max_width="500px", background_color="white"
        ),
        open=GrupoState.modal_editar_abierto,
        on_open_change=GrupoState.cambiar_estado_editar
    )

def tarjeta_grupo(grupo: Grupos) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(grupo.nombre, size="4", weight="bold", color="#111827"),
                rx.spacer(),
                
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.icon("ellipsis-vertical", size=18, color="#9ca3af"),
                            variant="ghost", size="1", color_scheme="gray", cursor="pointer"
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            rx.icon("send", size=14), "Enviar código por notificación", 
                            on_click=GrupoState.abrir_modal_envio(grupo.id_grupo, grupo.nombre, grupo.codigo_acceso),
                            cursor="pointer"
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            rx.icon("pencil", size=14), "Editar grupo", 
                            on_click=GrupoState.abrir_modal_editar(grupo.id_grupo, grupo.nombre, grupo.codigo_acceso),
                            cursor="pointer"
                        ),
                        rx.menu.item(
                            rx.icon("trash-2", size=14), "Eliminar grupo", 
                            on_click=GrupoState.eliminar_grupo(grupo.id_grupo),
                            color="#ef4444", cursor="pointer" 
                        )
                    )
                ),
                
                width="100%",
                align="center"
            ),
            rx.divider(margin_y="0.5em"),
            rx.hstack(
                rx.text("Código de acceso:", size="2", color="#6b7280"),
                rx.badge(
                    grupo.codigo_acceso, 
                    color_scheme="indigo", 
                    size="3", 
                    radius="large", 
                    variant="solid" 
                ),
                rx.button(
                    rx.icon("copy", size=14, color="#4b5563"),
                    size="1",
                    variant="soft", 
                    color_scheme="gray",
                    cursor="pointer",
                    on_click=[
                        rx.set_clipboard(grupo.codigo_acceso),
                        rx.toast.success("¡Código copiado!", position="bottom-right")
                    ]
                ),
                align="center",
                spacing="2"
            ),
            spacing="3",
            align_items="start"
        ),
        width="100%",
        box_shadow="sm",
        border="1px solid #e5e7eb",
        background_color="white"
    )

def docente_grupos_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo=""),
                
                rx.hstack(
                    rx.vstack(
                        rx.heading("Mis Grupos", size="8", weight="bold", color="#111827"),
                        rx.text("Administra tus clases y obtén los códigos de acceso.", color="#6b7280", size="3"),
                    ),
                    rx.spacer(),
                    modal_crear_grupo(),
                    width="100%", align="center", margin_bottom="2em"
                ),
                
                rx.cond(
                    GrupoState.mis_grupos.length() > 0,
                    rx.grid(
                        rx.foreach(GrupoState.mis_grupos, tarjeta_grupo),
                        columns={"initial": "1", "sm": "2", "md": "3"},
                        spacing="5",
                        width="100%"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("users", size=48, color="#9ca3af"),
                            rx.text("Aún no tienes grupos.", weight="bold", color="#374151"),
                            rx.text("Haz clic en 'Nuevo Grupo' para empezar.", color="#6b7280", size="2"),
                            align="center", spacing="2"
                        ),
                        padding="5em",
                        width="100%",
                        background_color="#ffffff",
                        border="2px dashed #e5e7eb",
                        border_radius="8px"
                    )
                ),
                
                modal_enviar_codigo_global(),
                modal_editar_grupo_global(),
                
                padding="3em", max_width="1000px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )

def render_estudiante(nombre: str) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=nombre[:2].upper(), size="1", radius="full", color_scheme="indigo"),
        rx.text(nombre, size="2", color="#374151", weight="medium"),
        rx.spacer(),
        rx.button(
            rx.cond(
                GrupoState.estudiantes_seleccionados.contains(nombre),
                rx.hstack(rx.icon("check", size=14), rx.text("Seleccionado", size="1")),
                rx.text("Añadir", size="1")
            ),
            on_click=GrupoState.toggle_estudiante(nombre),
            size="1",
            variant=rx.cond(GrupoState.estudiantes_seleccionados.contains(nombre), "solid", "soft"),
            color_scheme=rx.cond(GrupoState.estudiantes_seleccionados.contains(nombre), "green", "indigo"),
            cursor="pointer",
        ),
        width="100%", padding="0.75em", border_bottom="1px solid #f3f4f6", align="center"
    )

def render_miembro_actual(miembro: dict) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=miembro["iniciales"], size="1", radius="full", color_scheme="gray"),
        rx.text(miembro["nombre"], size="2", color="#374151"),
        rx.spacer(),
        rx.button(
            rx.icon("user-minus", size=14), "Expulsar",
            size="1", variant="soft", color_scheme="red", cursor="pointer",
            on_click=lambda: GrupoState.expulsar_miembro(miembro["id"].to(int), miembro["nombre"])
        ),
        width="100%", padding="0.5em", border_bottom="1px solid #f3f4f6", align="center"
    )

def render_candidato_invitar(nombre: str) -> rx.Component:
    return rx.hstack(
        rx.avatar(fallback=nombre[:2].upper(), size="1", radius="full", color_scheme="indigo"),
        rx.text(nombre, size="2", color="#374151"),
        rx.spacer(),
        rx.button(
            rx.cond(GrupoState.seleccionados_invitar.contains(nombre), rx.icon("check", size=14), rx.text("Invitar", size="1")),
            on_click=GrupoState.toggle_invitar(nombre),
            size="1",
            variant=rx.cond(GrupoState.seleccionados_invitar.contains(nombre), "solid", "soft"),
            color_scheme=rx.cond(GrupoState.seleccionados_invitar.contains(nombre), "green", "indigo"),
            cursor="pointer",
        ),
        width="100%", padding="0.5em", border_bottom="1px solid #f3f4f6", align="center"
    )