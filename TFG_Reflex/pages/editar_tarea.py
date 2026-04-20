import reflex as rx
from ..state.tarea_state import TareaState
from ..components.layout import sidebar_layout, header_component
from .crear_tarea import render_pregunta, render_estudiante_asignar


def editar_tarea_page() -> rx.Component:
    estilo_label = {"weight": "medium", "size": "2", "color": "#374151"}
    estilo_input = {"width": "100%", "background_color": "white", "border": "1px solid #d1d5db", "color": "#111827"}

    return rx.flex(
        sidebar_layout(),
        rx.box(
            rx.vstack(
                header_component(titulo="Editar Tarea"),
                rx.cond(
                    TareaState.error_edicion != "",
                    rx.center(
                        rx.vstack(
                            rx.icon("file-warning", size=48, color="#ef4444"),
                            rx.heading("No se puede editar la tarea", size="6", color="#111827"),
                            rx.text(TareaState.error_edicion, color="#6b7280", size="2"),
                            rx.button("Volver a mis tareas", on_click=rx.redirect("/mis-tareas"), color_scheme="indigo", cursor="pointer"),
                            align="center",
                            spacing="3",
                        ),
                        width="100%",
                        height="55vh",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.heading("Modificar tarea", size="5", color="#111827", weight="bold"),
                                rx.spacer(),
                                rx.button(
                                    rx.icon("arrow-left", size=16),
                                    "Volver",
                                    variant="ghost",
                                    color_scheme="gray",
                                    color="#4b5563",
                                    on_click=rx.redirect(f"/tarea/{TareaState.editando_tarea_id}"),
                                    cursor="pointer",
                                ),
                                width="100%",
                                align="center",
                            ),

                            rx.divider(margin_y="1em", background_color="#e5e7eb"),

                            rx.heading("1. Tipo de Actividad", size="4", color="#111827", weight="bold"),
                            rx.radio(
                                ["Ejercicio", "Prueba"],
                                direction="row",
                                on_change=TareaState.set_tipo_tarea,
                                value=TareaState.tipo_tarea,
                                spacing="4",
                                color_scheme="indigo",
                                size="2",
                                color="#374151",
                                weight="medium",
                            ),

                            rx.divider(margin_y="1.5em", background_color="#e5e7eb"),

                            rx.heading("2. Información General", size="4", color="#111827", weight="bold"),
                            rx.vstack(
                                rx.text("Título de la tarea", **estilo_label),
                                rx.input(
                                    value=TareaState.titulo,
                                    placeholder="Ej: Patrón Singleton en Python",
                                    on_change=TareaState.set_titulo,
                                    **estilo_input,
                                ),
                                spacing="1",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Descripción / Instrucciones Generales", **estilo_label),
                                rx.text_area(
                                    value=TareaState.descripcion,
                                    placeholder="Explica qué deben hacer...",
                                    on_change=TareaState.set_descripcion,
                                    min_height="100px",
                                    **estilo_input,
                                ),
                                spacing="1",
                                width="100%",
                                margin_top="0.5em",
                            ),

                            rx.cond(
                                TareaState.tipo_tarea == "Prueba",
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Fecha de Apertura", **estilo_label),
                                        rx.box(
                                            rx.input(id="edit_fecha_inicio", type="datetime-local", value=TareaState.fecha_inicio, on_change=TareaState.set_fecha_inicio, **estilo_input, padding_right="2.5em"),
                                            rx.icon("calendar-days", position="absolute", right="0.75em", top="50%", transform="translateY(-50%)", color="#6b7280", _hover={"color": "#111827"}, on_click=rx.call_script("document.getElementById('edit_fecha_inicio').showPicker()"), cursor="pointer"),
                                            position="relative",
                                            width="100%",
                                        ),
                                        width="100%",
                                        spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Fecha Límite / Cierre", **estilo_label),
                                        rx.box(
                                            rx.input(id="edit_fecha_fin", type="datetime-local", value=TareaState.fecha_fin, on_change=TareaState.set_fecha_fin, **estilo_input, padding_right="2.5em"),
                                            rx.icon("calendar-days", position="absolute", right="0.75em", top="50%", transform="translateY(-50%)", color="#6b7280", _hover={"color": "#111827"}, on_click=rx.call_script("document.getElementById('edit_fecha_fin').showPicker()"), cursor="pointer"),
                                            position="relative",
                                            width="100%",
                                        ),
                                        width="100%",
                                        spacing="1",
                                    ),
                                    width="100%",
                                    spacing="5",
                                    margin_top="0.5em",
                                ),
                            ),

                            rx.divider(margin_y="1.5em", background_color="#e5e7eb"),

                            rx.heading("3. Configuraciones Específicas", size="4", color="#111827", weight="bold"),
                            rx.cond(
                                TareaState.tipo_tarea == "Ejercicio",
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Dificultad", **estilo_label),
                                        rx.select(["facil", "medio", "dificil"], value=TareaState.nivel_dificultad, on_change=TareaState.set_nivel_dificultad, **estilo_input),
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        rx.text("Opciones", **estilo_label),
                                        rx.hstack(
                                            rx.checkbox(checked=TareaState.permite_reintentos, on_change=TareaState.set_permite_reintentos, color_scheme="indigo", size="2", cursor="pointer"),
                                            rx.text("Permitir reintentos", color="#111827", weight="medium", size="2"),
                                            align="center",
                                            spacing="2",
                                        ),
                                        justify="center",
                                        height="100%",
                                    ),
                                    spacing="5",
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Tiempo Límite Calculado", **estilo_label),
                                    rx.box(
                                        rx.text(TareaState.tiempo_limite_calculado, weight="bold", color=rx.cond(TareaState.tiempo_limite_calculado.contains("Error"), "#dc2626", "#111827")),
                                        padding="0.5em 1em",
                                        background_color=rx.cond(TareaState.tiempo_limite_calculado.contains("Error"), "#fee2e2", "#f3f4f6"),
                                        border_radius="6px",
                                        border=rx.cond(TareaState.tiempo_limite_calculado.contains("Error"), "1px solid #fca5a5", "1px solid #d1d5db"),
                                        width="100%",
                                        max_width="250px",
                                        display="flex",
                                        align_items="center",
                                    ),
                                    width="100%",
                                    align_items="start",
                                ),
                            ),

                            rx.divider(margin_y="1.5em", background_color="#e5e7eb"),

                            rx.heading("4. Preguntas", size="4", color="#111827", weight="bold"),
                            rx.vstack(
                                rx.foreach(TareaState.preguntas, lambda p, i: render_pregunta(p, i)),
                                width="100%",
                            ),
                            rx.cond(
                                TareaState.tipo_tarea == "Prueba",
                                rx.button(
                                    rx.hstack(rx.icon("plus", size=16), rx.text("Añadir otra pregunta")),
                                    on_click=TareaState.agregar_pregunta,
                                    variant="soft",
                                    color_scheme="indigo",
                                    width="100%",
                                    margin_top="1em",
                                    cursor="pointer",
                                ),
                            ),

                            rx.divider(margin_y="1.5em", background_color="#e5e7eb"),

                            rx.heading("5. Asignación", size="4", color="#111827", weight="bold"),
                            rx.radio(
                                ["Grupo", "Estudiantes"],
                                direction="row",
                                on_change=TareaState.set_tipo_asignacion,
                                value=TareaState.tipo_asignacion,
                                spacing="4",
                                color_scheme="indigo",
                                size="2",
                                color="#374151",
                                weight="medium",
                            ),
                            rx.cond(
                                TareaState.tipo_asignacion == "Grupo",
                                rx.select(
                                    items=TareaState.mis_grupos_nombres,
                                    value=TareaState.grupo_seleccionado_nombre,
                                    placeholder="Selecciona un grupo...",
                                    on_change=TareaState.set_grupo_por_nombre,
                                    **estilo_input,
                                    margin_top="1em",
                                ),
                                rx.vstack(
                                    rx.input(
                                        rx.input.slot(rx.icon("search", size=16, color="#9ca3af")),
                                        placeholder="Buscar alumno por nombre...",
                                        on_change=TareaState.set_busqueda_estudiante,
                                        **estilo_input,
                                    ),
                                    rx.box(
                                        rx.vstack(rx.foreach(TareaState.estudiantes_filtrados, render_estudiante_asignar), spacing="0"),
                                        max_height="220px",
                                        overflow="auto",
                                        border="1px solid #e5e7eb",
                                        border_radius="6px",
                                        background_color="white",
                                        width="100%",
                                    ),
                                    margin_top="1em",
                                    width="100%",
                                ),
                            ),

                            rx.button(
                                rx.hstack(rx.icon("save", size=18), rx.text("Guardar cambios")),
                                on_click=TareaState.actualizar_tarea,
                                color_scheme="indigo",
                                width="100%",
                                size="3",
                                margin_top="2.5em",
                                cursor="pointer",
                            ),
                            spacing="3",
                            width="100%",
                            align_items="start",
                        ),
                        width="100%",
                        padding="2.5em",
                        box_shadow="lg",
                        background_color="white",
                        border="1px solid #e5e7eb",
                        border_radius="12px",
                    ),
                ),
                padding="3em",
                max_width="850px",
                margin="0 auto",
                width="100%",
            ),
            flex="1",
            height="100vh",
            background_color="#f9fafb",
            overflow="auto",
        ),
        width="100%",
    )
