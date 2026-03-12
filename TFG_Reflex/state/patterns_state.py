import reflex as rx
import sqlmodel
import base64
import mimetypes
from .base_state import BaseState
from ..models.patrones import PatronDiseño

class PatternsState(BaseState):
    patrones_bd: list[PatronDiseño] = []
    
    busqueda: str = ""
    categoria_seleccionada: str = "Todas"
    modo_vista: str = "grid" 
    nuevo_nombre: str = ""
    nueva_categoria: str = "Creacionales"
    nueva_descripcion: str = ""
    nuevo_pseudocodigo: str = ""
    nuevas_ventajas: str = ""
    nuevas_desventajas: str = ""
    nuevos_ejemplos: str = ""
    error_creacion: str = ""

    def cargar_patrones(self):
        with rx.session() as session:
            if self.usuario_rol in ["admin", "docente"]:
                statement = sqlmodel.select(PatronDiseño)
            else:
                statement = sqlmodel.select(PatronDiseño).where(PatronDiseño.activo == True)
            
            self.patrones_bd = session.exec(statement).all()

    @rx.var
    def patrones_filtrados(self) -> list[dict]:
        resultado = []
        for p in self.patrones_bd:
            if self.busqueda.lower() not in p.nombre.lower() and self.busqueda.lower() not in p.descripcion.lower():
                continue
            
            if self.categoria_seleccionada != "Todas" and p.categoria != self.categoria_seleccionada:
                continue
            
            resultado.append({
                "id": str(p.id_patron),
                "nombre": p.nombre,
                "categoria": p.categoria,
                "descripcion": p.descripcion,
                "diagrama": p.diagrama if p.diagrama else "/placeholder.png", 
                "activo": p.activo
            })
        return resultado

    def set_categoria(self, categoria: str):
        self.categoria_seleccionada = categoria

    def set_modo_vista(self, modo: str):
        self.modo_vista = modo

    def toggle_estado_patron(self, id_patron: str):
        if self.usuario_rol not in ["admin", "docente"]:
            return
            
        with rx.session() as session:
            patron = session.exec(sqlmodel.select(PatronDiseño).where(PatronDiseño.id_patron == int(id_patron))).first()
            if patron:
                patron.activo = not patron.activo
                session.add(patron)
                session.commit()
                
        self.cargar_patrones()
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        
        if not self.nuevo_nombre.strip() or not self.nueva_descripcion.strip():
            self.error_creacion = "El nombre y la descripción son obligatorios."
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
            existente = session.exec(sqlmodel.select(PatronDiseño).where(PatronDiseño.nombre == self.nuevo_nombre.strip())).first()
            if existente:
                self.error_creacion = "Ya existe un patrón con este nombre."
                return

            nuevo_patron = PatronDiseño(
                nombre=self.nuevo_nombre.strip(),
                categoria=self.nueva_categoria,
                descripcion=self.nueva_descripcion.strip(),
                diagrama=cadena_base64_imagen if cadena_base64_imagen else "/placeholder.png",
                pseudocodigo=self.nuevo_pseudocodigo.strip(),
                ventajas=self.nuevas_ventajas.strip(),
                desventajas=self.nuevas_desventajas.strip(),
                ejemplos=self.nuevos_ejemplos.strip(),
                activo=True
            )
            session.add(nuevo_patron)
            session.commit()

        self.nuevo_nombre = ""
        self.nueva_categoria = "Creacionales"
        self.nueva_descripcion = ""
        self.nuevo_pseudocodigo = ""
        self.nuevas_ventajas = ""
        self.nuevas_desventajas = ""
        self.nuevos_ejemplos = ""
        self.error_creacion = ""
        self.cargar_patrones()
        return [
            rx.clear_selected_files("upload_diagrama"),
            rx.redirect("/biblioteca")
        ]