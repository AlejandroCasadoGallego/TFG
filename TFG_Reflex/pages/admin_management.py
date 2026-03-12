import reflex as rx
from ..state.admin_state import AdminState
from ..components.layout import sidebar_layout, header_component

# =======================================================
# DOCENTES
# =======================================================

def empty_state_docentes() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon("users", size=48, color="#9ca3af"),
            rx.heading("No hay docentes registrados", size="5", color="#111827", weight="bold"),
            rx.text("Añade el primer docente a la plataforma para empezar.", color="#6b7280", margin_bottom="1em"),
            align="center", spacing="3"
        ),
        padding="4em", border="2px dashed #e5e7eb", border_radius="12px", background_color="#f9fafb", width="100%"
    )

def render_fila_docente(docente: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.hstack(rx.avatar(fallback=docente["nombre"][:2], size="2", radius="full", color_scheme="cyan"), rx.text(docente["nombre"], weight="medium", color="#111827"), spacing="3", align="center")),
        rx.table.cell(rx.text(docente["correo"], color="#4b5563")),
        rx.table.cell(rx.badge(docente["estado"], color_scheme=rx.cond(docente["estado"] == "Activo", "green", "red"), variant="soft")),
        rx.table.cell(rx.button(rx.cond(docente["estado"] == "Activo", "Desactivar", "Activar"), on_click=lambda: AdminState.toggle_estado_docente(docente["id"]), color_scheme=rx.cond(docente["estado"] == "Activo", "red", "green"), variant="soft", size="1", cursor="pointer")),
        align="center"
    )

def gestion_docentes_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(),
                rx.hstack(
                    rx.vstack(rx.heading("Gestión de Docentes", size="7", color="#111827", weight="bold"), rx.text("Administra los profesores de la plataforma.", color="#6b7280", size="2")),
                    rx.spacer(),
                    rx.dialog.root(
                        rx.dialog.trigger(rx.button(rx.icon("plus", size=18), "Añadir Docente", color_scheme="indigo", cursor="pointer")),
                        rx.dialog.content(
                            rx.hstack(rx.dialog.title("Registrar Nuevo Docente", color="#111827", margin="0"), rx.dialog.close(rx.button(rx.icon("x", size=20, color="#6b7280"), variant="ghost", cursor="pointer", padding="0.2em")), justify="between", align="center", width="100%"),
                            rx.dialog.description("Completa los datos para dar de alta a un profesor.", color="#4b5563", margin_top="0.5em", margin_bottom="1.5em"),
                            rx.vstack(
                                rx.text("Nombre Completo", weight="bold", size="2", color="#374151"), rx.input(placeholder="Ej: Laura García", value=AdminState.new_doc_nombre, on_change=AdminState.set_new_doc_nombre, width="100%", background_color="white", color="#111827", border="1px solid #d1d5db"),
                                rx.text("Correo Electrónico", weight="bold", size="2", color="#374151", margin_top="0.5em"), rx.input(placeholder="docente@universidad.es", value=AdminState.new_doc_correo, on_change=AdminState.set_new_doc_correo, width="100%", background_color="white", color="#111827", border="1px solid #d1d5db"),
                                rx.text("Contraseña de acceso", weight="bold", size="2", color="#374151", margin_top="0.5em"), rx.input(type="password", placeholder="••••••••", value=AdminState.new_doc_pass, on_change=AdminState.set_new_doc_pass, width="100%", background_color="white", color="#111827", border="1px solid #d1d5db"),
                                width="100%", spacing="2"
                            ),
                            rx.cond(AdminState.error_new_doc != "", rx.text(AdminState.error_new_doc, color="#ef4444", size="2", weight="medium", margin_top="1em")),
                            rx.flex(rx.dialog.close(rx.button("Cancelar", background_color="#f3f4f6", color="#374151", border="1px solid #d1d5db", cursor="pointer")), rx.button("Crear Docente", on_click=AdminState.registrar_docente, color_scheme="indigo", cursor="pointer"), spacing="3", margin_top="2em", justify="end"),
                            background_color="#ffffff",
                        )
                    ),
                    width="100%", align="center", margin_bottom="2em"
                ),
                rx.card(
                    rx.cond(
                        AdminState.lista_docentes.length() > 0,
                        rx.table.root(
                            rx.table.header(rx.table.row(rx.table.column_header_cell("Usuario", color="#4b5563"), rx.table.column_header_cell("Correo", color="#4b5563"), rx.table.column_header_cell("Estado", color="#4b5563"), rx.table.column_header_cell("Acciones", color="#4b5563"))),
                            rx.table.body(rx.foreach(AdminState.lista_docentes, render_fila_docente)), width="100%", variant="surface"
                        ),
                        empty_state_docentes()
                    ),
                    width="100%", padding="1.5em", background_color="white", box_shadow="sm", border="1px solid #e5e7eb"
                ),
                padding="3em", max_width="1200px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )

# =======================================================
# ESTUDIANTES
# =======================================================

def empty_state_estudiantes() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon("users", size=48, color="#9ca3af"),
            rx.heading("No hay estudiantes registrados", size="5", color="#111827", weight="bold"),
            rx.text("Los alumnos aparecerán aquí automáticamente cuando se registren desde la página principal.", color="#6b7280", text_align="center"),
            align="center", spacing="3"
        ),
        padding="4em", border="2px dashed #e5e7eb", border_radius="12px", background_color="#f9fafb", width="100%"
    )

def render_fila_estudiante(estudiante: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.hstack(rx.avatar(fallback=estudiante["nombre"][:2], size="2", radius="full", color_scheme="green"), rx.text(estudiante["nombre"], weight="medium", color="#111827"), spacing="3", align="center")),
        rx.table.cell(rx.text(estudiante["correo"], color="#4b5563")),
        rx.table.cell(rx.badge(estudiante["estado"], color_scheme=rx.cond(estudiante["estado"] == "Activo", "green", "red"), variant="soft")),
        rx.table.cell(rx.button(rx.cond(estudiante["estado"] == "Activo", "Desactivar", "Activar"), on_click=lambda: AdminState.toggle_estado_estudiante(estudiante["id"]), color_scheme=rx.cond(estudiante["estado"] == "Activo", "red", "green"), variant="soft", size="1", cursor="pointer")),
        align="center"
    )

def gestion_estudiantes_page() -> rx.Component:
    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(),
                rx.hstack(rx.vstack(rx.heading("Gestión de Estudiantes", size="7", color="#111827", weight="bold"), rx.text("Administra las cuentas de los alumnos de la plataforma.", color="#6b7280", size="2")), rx.spacer(), width="100%", align="center", margin_bottom="2em"),
                rx.card(
                    rx.cond(
                        AdminState.lista_estudiantes.length() > 0,
                        rx.table.root(
                            rx.table.header(rx.table.row(rx.table.column_header_cell("Usuario", color="#4b5563"), rx.table.column_header_cell("Correo", color="#4b5563"), rx.table.column_header_cell("Estado", color="#4b5563"), rx.table.column_header_cell("Acciones", color="#4b5563"))),
                            rx.table.body(rx.foreach(AdminState.lista_estudiantes, render_fila_estudiante)), width="100%", variant="surface"
                        ),
                        empty_state_estudiantes()
                    ),
                    width="100%", padding="1.5em", background_color="white", box_shadow="sm", border="1px solid #e5e7eb"
                ),
                padding="3em", max_width="1200px", margin="0 auto", width="100%"
            ),
            flex="1", height="100vh", background_color="#f9fafb", overflow="auto"
        ),
        width="100%"
    )