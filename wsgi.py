from app import create_app
from config import ProductionConfig

# Instancia de la aplicación usando la configuración de Producción
app = create_app(ProductionConfig)

if __name__ == "__main__":
    # Esto solo corre si haces: python wsgi.py
    app.run(host="0.0.0.0", port=5000)
