RUBIK CRUD — FastAPI + SQLModel + Cloudinary

Sistema completo para gestionar Cubos Rubik, Competidores, Torneos y Récords.
Incluye diseño moderno, subida de imágenes a Cloudinary y CRUDs completos.

TECNOLOGÍAS PRINCIPALES

FastAPI → Backend
SQLModel → ORM + Base de datos
SQLite / PostgreSQL → Almacenamiento
Jinja2 → Plantillas HTML
Cloudinary → Gestión y subida de imágenes
Uvicorn → Servidor
Python-dotenv → Variables de entorno

FUNCIONALIDADES

✔ CRUD de Cubos
✔ CRUD de Competidores con fotos
✔ CRUD de Torneos
✔ CRUD de Récords
✔ Interfaz moderna tipo glassmorphism
✔ Totalmente responsive
✔ Almacenamiento de imágenes en Cloudinary

ESTRUCTURA DEL PROYECTO

project/
main.py
requirements.txt
.env
cloudinary_config.py

database/
db.py

models/
cube.py
competitor.py
competitor_record.py
tournament.py

static/
styles.css

templates/
base.html
index.html
cube_list.html
cube_form.html
competitor_list.html
competitor_form.html
competitor_edit.html
tournament_list.html
tournament_form.html
tournament_edit.html
record_list.html
record_form.html
record_edit.html

INSTALACIÓN Y CONFIGURACIÓN

Clonar el repositorio
git clone https://github.com/tuusuario/rubik-crud.git

cd rubik-crud

Instalar dependencias
pip install -r requirements.txt

Crear archivo .env
CLOUDINARY_CLOUD_NAME=tu_nombre
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

Ejecutar servidor
uvicorn main:app --reload

Abrir en navegador:
http://127.0.0.1:8000

SUBIDA DE IMÁGENES (CLOUDINARY)

El sistema sube imágenes con:

result = cloudinary.uploader.upload(image.file)
image_url = result["secure_url"]

La URL se guarda en la BD y se usa en las vistas.

MODELOS (RELACIONES)

Cube (1) → (∞) Competitor → (∞) CompetitorRecord
Tournament (1) → (∞) Competitor
Tournament (1) → (∞) CompetitorRecord
Cube (1) → (∞) CompetitorRecord

INTERFAZ Y DISEÑO

• Estilo glassmorphism
• Sombras y efectos neon
• Tarjetas de competidores
• Tablas con bordes redondeados
• Diseño responsive
• Imágenes redondas con borde de brillo

REQUIREMENTS 

fastapi
uvicorn
sqlmodel
jinja2
python-multipart
cloudinary
python-dotenv

CONTRIBUIR

Hacer fork

Crear una rama

Subir cambios

Abrir Pull Request


