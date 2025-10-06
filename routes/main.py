from datetime import date
from calendar import monthcalendar
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import WorkoutLog, Exercise
from app import db
from sqlalchemy import func, extract

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # --- Manejo de mes y año desde la URL ---
    try:
        year = int(request.args.get('year', date.today().year))
        month = int(request.args.get('month', date.today().month))
        if not (1 <= month <= 12):
            raise ValueError
    except (ValueError, TypeError):
        # Si los parámetros son inválidos, redirigir a hoy
        return redirect(url_for('main.index'))

    # --- Obtener logs del usuario en ese mes ---
    logs = WorkoutLog.query.filter(
        WorkoutLog.user_id == current_user.user_id,
        extract('year', WorkoutLog.date) == year,
        extract('month', WorkoutLog.date) == month
    ).all()

    workout_days = {log.date.day for log in logs}
    cal = monthcalendar(year, month)
    today = date.today()

    # --- Estadísticas ---
    # Días entrenados en el mes
    days_this_month = len(workout_days)

    # Total de logs del usuario
    total_logs = WorkoutLog.query.filter_by(user_id=current_user.user_id).count()

    # Ejercicio más frecuente
    most_frequent = (
        db.session.query(Exercise.name, func.count(WorkoutLog.exercise_id).label("freq"))
        .join(WorkoutLog.exercise)
        .filter(WorkoutLog.user_id == current_user.user_id)
        .group_by(Exercise.name)
        .order_by(func.count(WorkoutLog.exercise_id).desc())
        .first()
    )

    return render_template(
        'main/index.html',
        cal=cal,
        year=year,
        month=month,
        workout_days=workout_days,
        today=today,
        # stats
        days_this_month=days_this_month,
        total_logs=total_logs,
        most_frequent=most_frequent[0] if most_frequent else None
    )

@bp.route('/about')
def about():
    return render_template("main/about.html")

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        if not name or not email or not message:
            flash("Todos los campos son obligatorios.", "danger")
        else:
            # Aquí podrías enviar email o guardar en DB
            flash("Gracias por contactarnos, te responderemos pronto.", "success")
            return redirect(url_for("main.contact"))
        
    return render_template("main/contact.html")