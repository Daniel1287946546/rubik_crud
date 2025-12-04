RUBIK CRUD — FastAPI + SQLModel + Cloudinary

Sistema completo para gestionar Cubos Rubik, Competidores, Torneos y Récords oficiales.
Incluye CRUDs completos, subida de imágenes con Cloudinary, diseño moderno y arquitectura modular.


Tecnologías Principales

🧩 FastAPI               → Backend  
🗄️ SQLModel             → ORM + Base de datos  
🐘 PostgreSQL / SQLite  → Almacenamiento  
🎨 Jinja2               → Templates HTML  
🌩️ Cloudinary           → Subida de imágenes  
🚀 Uvicorn              → Servidor ASGI  
🔐 python-dotenv        → Variables de entorno  

Estructuta 
project/
│── main.py
│── requirements.txt
│── cloudinary_config.py
│── .env
│
├── database/
│   └── db.py
│
├── models/
│   ├── cube.py
│   ├── competitor.py
│   ├── competitor_record.py
│   └── tournament.py
│
├── routers/
│   ├── cube_router.py
│   ├── competitor_router.py
│   ├── tournament_router.py
│   └── record_router.py
│
├── static/
│   ├── styles.css
│   └── uploads/
│
└── templates/
    ├── base.html
    ├── index.html
    ├── cube_list.html
    ├── cube_form.html
    ├── cube_edit.html
    ├── competitor_list.html
    ├── competitor_form.html
    ├── competitor_edit.html
    ├── tournament_list.html
    ├── tournament_form.html
    ├── tournament_edit.html
    ├── record_list.html
    ├── record_form.html
    └── record_edit.html


| Relación                      | Tipo | Descripción                                               |
| ----------------------------- | ---- | --------------------------------------------------------- |
| Tournament → Competitor       | 1:N  | Un torneo puede tener múltiples competidores registrados. |
| Tournament → CompetitorRecord | 1:N  | Un torneo puede tener múltiples récords asociados.        |
| Cube → Competitor             | 1:N  | Un cubo puede estar asociado a múltiples competidores.    |
| Cube → CompetitorRecord       | 1:N  | Un cubo puede registrar múltiples récords.                |
| Competitor → CompetitorRecord | 1:N  | Un competidor puede tener múltiples récords.              |


Mapa de EndPoins
| Método | Endpoint            | Descripción                           |
| ------ | ------------------- | ------------------------------------- |
| GET    | `/competitors`      | Lista todos los competidores          |
| GET    | `/competitors/{id}` | Consulta un competidor por ID         |
| POST   | `/competitors`      | Crea un nuevo competidor              |
| PUT    | `/competitors/{id}` | Actualiza completamente un competidor |
| DELETE | `/competitors/{id}` | Elimina un competidor                 |



Cubes

| Método | Endpoint      | Descripción             |
| ------ | ------------- | ----------------------- |
| GET    | `/cubes`      | Lista todos los cubos   |
| GET    | `/cubes/{id}` | Consulta un cubo por ID |
| POST   | `/cubes`      | Crea un nuevo cubo      |
| PUT    | `/cubes/{id}` | Actualiza un cubo       |
| DELETE | `/cubes/{id}` | Elimina un cubo         |


Tournaments

| Método | Endpoint            | Descripción               |
| ------ | ------------------- | ------------------------- |
| GET    | `/tournaments`      | Lista todos los torneos   |
| GET    | `/tournaments/{id}` | Consulta un torneo por ID |
| POST   | `/tournaments`      | Crea un torneo            |
| PUT    | `/tournaments/{id}` | Actualiza un torneo       |
| DELETE | `/tournaments/{id}` | Elimina un torneo         |

Records

| Método | Endpoint        | Descripción               |
| ------ | --------------- | ------------------------- |
| GET    | `/records`      | Lista todos los récords   |
| GET    | `/records/{id}` | Consulta un récord por ID |
| POST   | `/records`      | Crea un nuevo récord      |
| PUT    | `/records/{id}` | Actualiza un récord       |
| DELETE | `/records/{id}` | Elimina un récord         |


Instalación y Configuración

git clone https://github.com/Daniel1287946546/rubik_crud.git
cd rubik_crud

instalar dependencias
pip install -r requirements.txt

Crear env.
CLOUDINARY_CLOUD_NAME=tu_cloud
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret


ejecutar en el servidor

uvicorn main:app --reload

Abrir en navegador: http://127.0.0.1:8000



Subida de Imágenes (Cloudinary)

result = cloudinary.uploader.upload(image.file)
image_url = result["secure_url"]


Requirements
fastapi
uvicorn
sqlmodel
jinja2
python-multipart
cloudinary
python-dotenv



