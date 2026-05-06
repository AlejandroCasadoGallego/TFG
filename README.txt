PATTERNLAB (TFG REFLEX)
=======================

Plataforma educativa interactiva desarrollada como Trabajo de Fin de Grado (TFG). Permite la gestion de grupos, resolucion de tareas, biblioteca de patrones arquitectonicos, y un completo seguimiento del progreso de los estudiantes.

--- TECNOLOGIAS UTILIZADAS ---
- Framework: Reflex (Python full-stack framework)
- Lenguaje: Python 3.10+
- Base de Datos: desarrollo local
- ORM: SQLModel / SQLAlchemy
- UI: Componentes de interfaz generados mediante Reflex (Radix UI)

--- REQUISITOS PREVIOS ---
Asegurate de tener instalado en tu sistema:
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

--- INSTALACION Y CONFIGURACION LOCAL ---
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

--- EJECUCION DEL SERVIDOR DE DESARROLLO ---
Para iniciar la aplicacion en modo desarrollo (con recarga automatica):
   reflex run

La aplicacion estara disponible en tu navegador en: http://localhost:3000

--- ESTRUCTURA DEL PROYECTO ---
- TFG_Reflex/ : Directorio principal del codigo fuente.
  - components/ : Componentes de interfaz reutilizables (layout, barra lateral, tarjetas).
  - models/ : Esquemas de base de datos SQLModel (Usuarios, Tareas, Grupos).
  - pages/ : Vistas y rutas de la aplicacion (Dashboard, Tareas, Evaluaciones).
  - state/ : Logica de negocio y gestion de estados de Reflex.
  - colores.py : Paleta de colores centralizada del sistema de diseno.
- assets/ : Archivos estaticos e imagenes.
- rxconfig.py : Configuracion global de la aplicacion Reflex y URL de la base de datos.
- alembic/ : Historial y configuracion de migraciones de base de datos.

--- CONFIGURACION DE BASE DE DATOS (PRODUCCION) ---
Por defecto, el proyecto usa una base de datos local. Para entornos de produccion o Reflex Cloud, debes modificar la variable database_url en rxconfig.py para apuntar a un servicio MySQL externo:

import reflex as rx

--- ROLES DE USUARIO ---
El sistema soporta 3 tipos de acceso:
1. Estudiante: Acceso a grupos, resolucion de tareas, resumen academico y notificaciones.
2. Docente: Creacion y correccion de tareas, gestion de grupos, y liberacion manual de calificaciones.
3. Administrador: Gestion del sistema, control de usuarios (alta/baja de docentes y estudiantes), y reseteo de contrasenas.