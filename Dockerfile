# Imagen base oficial de Python
FROM python:3.11-slim

# Evitar mensajes interactivos de pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Copiar requerimientos
COPY requirements.txt .

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto Flask
EXPOSE 5000

# Comando por defecto: ejecutar la app
CMD ["flask", "run", "--host=0.0.0.0"]
