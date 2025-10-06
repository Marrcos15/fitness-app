# 🏋️‍♂️ Gym Routine App

Aplicación web desarrollada con **Flask**, **Bootstrap** y **PostgreSQL** para gestionar rutinas de gimnasio, registrar entrenamientos y visualizar el progreso de los usuarios.

---

## 🚀 Funcionalidades principales

- ✅ Registro e inicio de sesión de usuarios  
- ✅ Roles de usuario (usuario / administrador)  
- ✅ CRUD de ejercicios y rutinas  
- ✅ Importación masiva de datos desde archivos CSV  
- ✅ Registro diario de entrenamientos (Workout Logs)  
- ✅ Historial y calendario de entrenamientos  
- ✅ Panel de usuario con actividad reciente  
- ✅ Diseño responsive con Bootstrap 5  
- ✅ Validaciones personalizadas y seguridad con CSRF  
- ✅ Migraciones con Flask-Migrate (Alembic)  
- ✅ Despliegue con Docker + PostgreSQL  

---

## 🧱 Estructura del proyecto

```
fitness-app/
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── forms.py
├── seed.py
│
├── models/
│   ├── user.py
│   ├── exercise.py
│   ├── routine.py
│   ├── workout_log.py
│   ├── equipment.py
│   ├── muscle_group.py
│   ├── difficulty_level.py
│   └── associations.py
│
├── routes/
│   ├── main.py
│   ├── auth.py
│   ├── users.py
│   ├── exercises.py
│   ├── routines.py
│   └── workout_logs.py
│
├── templates/
│   ├── auth/
│   ├── exercises/
│   ├── routines/
│   ├── users/
│   ├── workout_logs/
│   └── partials/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── examples/
│
├── utils/
│   ├── helpers.py
│   ├── validators.py
│   └── decorators.py
│
└── migrations/
```

---

## ⚙️ Instalación local (modo desarrollo)

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Marrcos15/fitness-app.git
cd fitness-app
```

### 2️⃣ Crear y activar entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En macOS / Linux
venv\Scripts\activate     # En Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las variables del `.env.example`

### 5️⃣ Inicializar la base de datos

```bash
flask db init
flask db migrate -m "message"
flask db upgrade
flask run
```

### 6️⃣ Carga de datos de ejemplo
```python
python seed.py
```

La aplicación estará disponible en:  
👉 http://127.0.0.1:5000

El login con los datos de prueba es:
- user: correo@example.com
- password: 123456
---

## 🐳 Despliegue con Docker + PostgreSQL

### 1️⃣ Configurar el archivo `.env`

Ejemplo de configuración para producción:

```
SECRET_KEY=supersecretkey
DB_NAME=fitnessdb
DB_USER=fitadmin
DB_PASSWORD=securepass
DB_HOST=db
DB_PORT=5432
```

### 2️⃣ Levantar los contenedores

```bash
docker-compose up --build
```

Esto lanzará:
- `web` → Flask App en http://localhost:5000  
- `db` → PostgreSQL en puerto 5432 con persistencia

### 3️⃣ Ejecutar migraciones dentro del contenedor

```bash
docker exec -it fitness_app flask db upgrade
```

---

## 🧩 Importación de datos desde CSV

### 📁 Importar ejercicios

Ruta: `/exercises/import`

Formato esperado del CSV:

```csv
name,description,equipment,difficulty,muscle_groups
Press de banca,Ejercicio de pecho,Banco,Difícil,Pecho|Tríceps
Sentadilla,Ejercicio de piernas,Barra,Media,Piernas|Glúteos
Curl de bíceps,Ejercicio de brazos,Mancuernas,Fácil,Bíceps
```

---

### 📁 Importar rutinas

Ruta: `/routines/import`

Formato esperado del CSV:

```csv
month,year,day_name,exercise_names
1,2025,Lunes,Press de banca|Sentadilla|Curl de bíceps
1,2025,Martes,Plancha|Dominadas
```

---

## 👮 Roles y permisos

| Rol | Permisos |
|-----|-----------|
| Usuario normal | Registrar entrenamientos, ver rutinas |
| Administrador | Crear, editar y borrar ejercicios y rutinas, gestionar usuarios, importar datos CSV |

---

## 🧪 Migraciones con Alembic

Ejecutar dentro del contenedor o en local:

```bash
flask db migrate -m "mensaje de migración"
flask db upgrade
```

---

## 💾 Backups de la base de datos (PostgreSQL)

```bash
docker exec -t fitness_db pg_dump -U postgres fitnessdb > backup.sql
```

---

## 🧑‍💻 Autor

**Marcos**  
💼 Desarrollador Python
📧 Contacto: [mgonzalez.trabajo.18@gmail.com](mailto:mgonzalez.trabajo.18@gmail.com)

---

## 🪪 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

---

## 💡 Notas finales

- El proyecto está listo para ser desplegado en plataformas como **Render**, **Railway**, **Fly.io**, **AWS ECS** o cualquier entorno Docker.  
- Si deseas probarlo localmente con SQLite, elimina las variables de entorno de PostgreSQL y crea una para SQLite.  
- El diseño está construido sobre **Bootstrap 5**, completamente responsive y adaptable a dispositivos móviles.
