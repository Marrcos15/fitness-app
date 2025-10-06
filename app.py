from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask import render_template
from utils.helpers import is_active, register_error_handlers
from utils.decorators import limiter
from datetime import datetime

# Declarar extensiones en el ámbito global del módulo
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Inicializar el limitador de tasa
    limiter.init_app(app)
    register_error_handlers(app)

    #Registrar rutas
    from routes.auth import bp as auth_bp
    from routes.main import bp as main_bp
    from routes.exercises import bp as exe_bp
    from routes.routines import bp as routine_bp
    from routes.workout_logs import bp as wkout_bp
    from routes.users import bp as user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(exe_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(routine_bp)
    app.register_blueprint(wkout_bp)
    app.register_blueprint(user_bp)

    # Manejadores de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    # Context processor para helpers
    @app.context_processor
    def utility_processor():
        return dict(is_active=is_active)
    @app.context_processor
    def inject_now():
        return {"current_year": datetime.utcnow().year}

    return app

# Punto de entrada
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)