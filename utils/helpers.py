from flask import request, flash, redirect, url_for, get_flashed_messages
from flask_limiter.errors import RateLimitExceeded

def is_active(*prefixes: str) -> str:
    """
    Devuelve 'active' si el endpoint actual coincide con alguno de los prefijos indicados.
    Coincide si es exactamente el prefijo o si empieza por 'prefijo.' (blueprint.función).
    """
    ep = request.endpoint or ""
    for p in prefixes:
        if ep == p or ep.startswith(p + "."):
            return "active"
    return ""


def register_error_handlers(app):
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        mensajes = get_flashed_messages()
        if "Has excedido el límite de solicitudes. Por favor, inténtalo más tarde." not in mensajes:
            flash("Has excedido el límite de solicitudes. Por favor, inténtalo más tarde.", "warning")
        return redirect(url_for('auth.login'))

