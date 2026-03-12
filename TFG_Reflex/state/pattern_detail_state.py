import reflex as rx
import sqlmodel
import base64
import tempfile
import os
from fpdf import FPDF
from .base_state import BaseState
from ..models.patrones import PatronDiseño

class PatternDetailState(BaseState):
    """Maneja la vista de detalle de un patrón específico usando rutas dinámicas."""
    
    # 1. ¡HEMOS BORRADO id_patron: str = ""! Ya no "pisamos" a Reflex.
    
    patron_actual: dict = {}
    error_carga: bool = False

    def cargar_patron(self):
        """Busca el patrón en la BD usando el ID de la URL."""
        # 2. Leemos el ID dinámico directamente desde el router interno de Reflex
        id_url = self.router.page.params.get("id_patron", "")
        
        if not id_url:
            return
            
        with rx.session() as session:
            patron = session.exec(
                sqlmodel.select(PatronDiseño).where(PatronDiseño.id_patron == int(id_url))
            ).first()
            
            if patron:
                # Si el usuario es estudiante/visitante y el patrón está inactivo, lo bloqueamos
                if not patron.activo and self.usuario_rol not in ["admin", "docente"]:
                    self.error_carga = True
                    return

                self.patron_actual = {
                    "id": str(patron.id_patron),
                    "nombre": patron.nombre,
                    "categoria": patron.categoria,
                    "descripcion": patron.descripcion,
                    "diagrama": patron.diagrama if patron.diagrama else "/placeholder.png",
                    "pseudocodigo": patron.pseudocodigo,
                    "ventajas": patron.ventajas,
                    "desventajas": patron.desventajas,
                    "ejemplos": patron.ejemplos,
                    "activo": patron.activo
                }
                self.error_carga = False
            else:
                self.error_carga = True

    def toggle_estado_actual(self):
        """Activa o desactiva el patrón desde la vista de detalle."""
        if self.usuario_rol not in ["admin", "docente"]:
            return
            
        # Volvemos a leer el ID de la URL
        id_url = self.router.page.params.get("id_patron", "")
        if not id_url:
            return

        with rx.session() as session:
            patron = session.exec(sqlmodel.select(PatronDiseño).where(PatronDiseño.id_patron == int(id_url))).first()
            if patron:
                patron.activo = not patron.activo
                session.add(patron)
                session.commit()
                self.cargar_patron() # Recargamos para actualizar la UI

    async def descargar_pdf(self):
        """Genera un PDF al vuelo con los datos del patrón y lo descarga."""
        if not self.patron_actual:
            return

        # 1. Inicializamos el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # 2. Título y Categoría
        pdf.set_font("helvetica", style="B", size=24)
        pdf.set_text_color(17, 24, 39) # Gris muy oscuro
        pdf.cell(0, 10, self.patron_actual["nombre"], new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_font("helvetica", style="I", size=14)
        pdf.set_text_color(107, 114, 128) # Gris medio
        pdf.cell(0, 10, f"Categoría: {self.patron_actual['categoria']}", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(10) # Salto de línea

        # 3. Procesar la Imagen Base64 (El truco maestro)
        # Como guardamos la imagen en Base64, necesitamos decodificarla 
        # a un archivo temporal para que FPDF pueda leerla
        img_data = self.patron_actual["diagrama"]
        if img_data and img_data.startswith("data:image"):
            try:
                # Separamos la cabecera del contenido real
                header, encoded = img_data.split(",", 1)
                img_bytes = base64.b64decode(encoded)
                
                # Creamos un archivo temporal físico
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(img_bytes)
                    tmp_path = tmp_file.name
                
                # Insertamos la imagen en el PDF centrada
                pdf.image(tmp_path, x="CENTER", w=120)
                pdf.ln(5)
                
                # Borramos el archivo temporal para no dejar basura en el servidor
                os.remove(tmp_path)
            except Exception as e:
                print(f"Error procesando imagen para PDF: {e}")
        
        # 4. Función de ayuda para imprimir secciones
        def imprimir_seccion(titulo, contenido):
            if contenido:
                pdf.set_font("helvetica", style="B", size=16)
                pdf.set_text_color(17, 24, 39)
                pdf.cell(0, 10, titulo, new_x="LMARGIN", new_y="NEXT")
                
                pdf.set_font("helvetica", size=12)
                pdf.set_text_color(55, 65, 81)
                # multi_cell maneja los saltos de línea automáticos
                pdf.multi_cell(0, 8, txt=contenido)
                pdf.ln(5)

        # 5. Volcamos la información
        imprimir_seccion("Descripción", self.patron_actual["descripcion"])
        imprimir_seccion("Ventajas", self.patron_actual["ventajas"])
        imprimir_seccion("Desventajas", self.patron_actual["desventajas"])
        imprimir_seccion("Ejemplos de Uso", self.patron_actual["ejemplos"])
        
        # Para el código usamos una fuente monoespaciada
        if self.patron_actual["pseudocodigo"]:
            pdf.set_font("helvetica", style="B", size=16)
            pdf.set_text_color(17, 24, 39)
            pdf.cell(0, 10, "Pseudocódigo", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("courier", size=10) # Fuente de código
            pdf.set_text_color(0, 0, 0)
            pdf.set_fill_color(243, 244, 246) # Fondo gris clarito
            pdf.multi_cell(0, 6, txt=self.patron_actual["pseudocodigo"], fill=True)

        # 6. Generamos el archivo en memoria y forzamos la descarga en Reflex
        pdf_bytes = bytes(pdf.output()) 
        
        # El nombre del archivo se limpiará para no tener espacios raros
        nombre_archivo = f"{self.patron_actual['nombre'].replace(' ', '_')}.pdf"
        
        return rx.download(data=pdf_bytes, filename=nombre_archivo)