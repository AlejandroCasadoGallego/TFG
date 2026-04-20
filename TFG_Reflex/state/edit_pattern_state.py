import reflex as rx
import sqlmodel
import mimetypes
import base64
from .base_state import BaseState
from ..models.patrones import PatronDiseño

class EditPatternState(BaseState):
    
    
    edit_nombre: str = ""
    edit_categoria: str = ""
    edit_descripcion: str = ""
    edit_pseudocodigo: str = ""
    edit_ventajas: str = ""
    edit_desventajas: str = ""
    edit_ejemplos: str = ""
    diagrama_actual: str = ""
    
    error_edicion: str = ""

    def cargar_datos(self):
        id_url = self.router.page.params.get("id_patron", "")
        if not id_url:
            return
            
        with rx.session() as session:
            patron = session.exec(sqlmodel.select(PatronDiseño).where(PatronDiseño.id_patron == int(id_url))).first()
            if patron:
                self.edit_nombre = patron.nombre
                self.edit_categoria = patron.categoria
                self.edit_descripcion = patron.descripcion
                self.edit_pseudocodigo = patron.pseudocodigo
                self.edit_ventajas = patron.ventajas
                self.edit_desventajas = patron.desventajas
                self.edit_ejemplos = patron.ejemplos
                self.diagrama_actual = patron.diagrama if patron.diagrama else "/placeholder.png"
                self.error_edicion = ""

    async def guardar_cambios(self, files: list[rx.UploadFile]):
        if not self.edit_nombre.strip() or not self.edit_descripcion.strip():
            self.error_edicion = "El nombre y la descripción son obligatorios."
            return

        id_url = self.router.page.params.get("id_patron", "")
        if not id_url:
            return

        cadena_base64_imagen = ""
        
        if files:
            upload_data = await files[0].read()
            nombre_archivo = files[0].filename
            mime_type, _ = mimetypes.guess_type(nombre_archivo)
            if not mime_type:
                mime_type = "image/png"
            img_base64 = base64.b64encode(upload_data).decode('utf-8')
            cadena_base64_imagen = f"data:{mime_type};base64,{img_base64}"
        with rx.session() as session:
            patron = session.exec(sqlmodel.select(PatronDiseño).where(PatronDiseño.id_patron == int(id_url))).first()
            if patron:
                existente = session.exec(sqlmodel.select(PatronDiseño).where((PatronDiseño.nombre == self.edit_nombre.strip()) & (PatronDiseño.id_patron != int(id_url)))).first()
                if existente:
                    self.error_edicion = "Ya existe otro patrón con este nombre."
                    return

                patron.nombre = self.edit_nombre.strip()
                patron.categoria = self.edit_categoria
                patron.descripcion = self.edit_descripcion.strip()
                patron.pseudocodigo = self.edit_pseudocodigo.strip()
                patron.ventajas = self.edit_ventajas.strip()
                patron.desventajas = self.edit_desventajas.strip()
                patron.ejemplos = self.edit_ejemplos.strip()
                
                if cadena_base64_imagen:
                    patron.diagrama = cadena_base64_imagen
                elif self.diagrama_actual == "/placeholder.png":
                    patron.diagrama = "/placeholder.png"
                    
                session.add(patron)
                session.commit()

        return [
            rx.clear_selected_files("upload_diagrama_edit"),
            rx.redirect(f"/patron/{id_url}")
        ]

    def eliminar_imagen_actual(self):
        self.diagrama_actual = "/placeholder.png"