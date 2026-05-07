PATTERNLAB (TFG REFLEX)
=======================

Plataforma educativa interactiva desarrollada como Trabajo de Fin de Grado (TFG). Permite la gestión de grupos, resolución de tareas, biblioteca de patrones arquitectónicos, y un completo seguimiento del progreso de los estudiantes.

--- TECNOLOGÍAS UTILIZADAS ---
- Framework: Reflex (Python full-stack framework)
- Lenguaje: Python 3.10+
- Base de Datos: desarrollo local
- ORM: SQLModel
- UI: Componentes de interfaz generados mediante Reflex (Radix UI)

--- REQUISITOS PREVIOS ---
Asegúrate de tener instalado en tu sistema:
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

--- INSTALACIÓN Y CONFIGURACIÓN LOCAL ---
Sigue estos pasos para desplegar el proyecto en tu entorno local:

1. Clonar el repositorio
   git clone https://github.com/AlejandroCasadoGallego/TFG
   cd TFG_Reflex

2. Crear y activar un entorno virtual
   - En Windows:
     python -m venv .venv
     .venv\Scripts\activate

   - En macOS / Linux:
     python3 -m venv .venv
     source .venv/bin/activate

3. Instalar dependencias
   pip install -r requirements.txt

4. Inicializar y aplicar migraciones de base de datos
   El proyecto utiliza Alembic para las migraciones. Para crear las tablas iniciales en la base de datos reflex.db ejecuta:
   reflex db init
   reflex db makemigrations
   reflex db migrate

--- EJECUCIÓN DEL SERVIDOR DE DESARROLLO ---
Para iniciar la aplicación en modo desarrollo (con recarga automática):
   reflex run

La aplicación estará disponible en tu navegador en: http://localhost:3000

--- ESTRUCTURA DEL PROYECTO ---
- TFG_Reflex/ : Directorio principal del código fuente.
  - components/ : Componentes de interfaz reutilizables (layout, barra lateral, tarjetas).
  - models/ : Esquemas de base de datos SQLModel (Usuarios, Tareas, Grupos).
  - pages/ : Vistas y rutas de la aplicación (Dashboard, Tareas, Evaluaciones).
  - state/ : Lógica de negocio y gestión de estados de Reflex.
  - colores.py : Paleta de colores centralizada del sistema de diseño.
- assets/ : Archivos estáticos e imágenes.
- rxconfig.py : Configuración global de la aplicación Reflex y URL de la base de datos.
- alembic/ : Historial y configuración de migraciones de base de datos.

--- CONFIGURACIÓN DE BASE DE DATOS (PRODUCCIÓN) ---
Por defecto, el proyecto usa una base de datos local. Para entornos de producción o Reflex Cloud, debes modificar la variable database_url en rxconfig.py para apuntar a un servicio MySQL externo.

--- ROLES DE USUARIO ---
El sistema soporta 3 tipos de acceso:
1. Estudiante: Acceso a grupos, resolución de tareas, resumen académico y notificaciones.
2. Docente: Creación y corrección de tareas, gestión de grupos, y liberación manual de calificaciones.
3. Administrador: Gestión del sistema, control de usuarios (alta/baja de docentes y estudiantes), y reseteo de contraseñas.