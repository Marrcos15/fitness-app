from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from datetime import date, datetime
from app import db
from models import RoutineDay, WorkoutLog, User


bp = Blueprint('workout_log', __name__, url_prefix='/workout')

@bp.route('/select_day', methods=['GET', 'POST'])
@login_required
def select_day():
    """ Muestra los días asociados a la rutina mensual para seleccionar el día para registrar los datos """
    routine_days = RoutineDay.query.all()
    if request.method == 'POST':
        day_id = request.form.get('day_id')
        return redirect(url_for('workout_log.add_workout', day_id=day_id))
    return render_template('workout/select_day.html', routine_days=routine_days)

@bp.route('/add/<int:day_id>', methods=['GET', 'POST'])
@login_required
def add_workout(day_id):
    routine_day = RoutineDay.query.get_or_404(day_id)
    exercises = routine_day.exercises

    if request.method == 'POST':
        errors = {}

        # Validar fecha
        date_str = request.form.get('date')
        try:
            chosen_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if chosen_date > date.today():
                errors['date'] = 'La fecha no puede ser futura.'
        except ValueError:
            errors['date'] = 'Formato de fecha inválido.'
        

        # Validar por cada ejercicio
        valid_logs = []
        for exercise in exercises:
            ex_err = {}
            sets_raw = request.form.get(f'sets_{exercise.exercise_id}').strip()
            reps_raw = request.form.get(f'reps_{exercise.exercise_id}').strip()
            weight_raw = request.form.get(f'weight_{exercise.exercise_id}').strip()
            notes = request.form.get(f'notes_{exercise.exercise_id}').strip()

            # Validar sets
            try:
                sets = int(sets_raw) if sets_raw else None
                if sets is None or sets < 1:
                    ex_err['sets'] = 'Las repeticiones deben ser un entero positivo.'
            except ValueError:
                ex_err['sets'] = 'Las repeticiones deben ser un entero válido.'

            # Validar reps
            try:
                reps = int(reps_raw) if reps_raw else None
                if reps is None or reps < 1:
                    ex_err['reps'] = 'Las series deben ser un entero positivo.'
            except ValueError:
                ex_err['reps'] = 'Las series deben ser un entero válido.'
            
            # Validar weight
            try:
                weight = float(weight_raw) if weight_raw else 0.0
                if weight < 0:
                    ex_err['weight'] = 'El peso no puede ser negativo.'
            except ValueError:
                ex_err['weight'] = 'El peso debe ser un número válido.'

            if ex_err:
                errors[exercise.exercise_id] = ex_err
            else:
                valid_logs.append({
                    'exercise_id': exercise.exercise_id,
                    'sets': sets,
                    'reps': reps,
                    'weight': weight,
                    'notes': notes
                })
        
        if errors:
            flash('Revisa los errores en el formulario.', 'danger')
            return render_template('workout/add_logs.html', routine_day=routine_day, exercises=exercises, errors=errors)
        
        # Guardar registros válidos
        for item in valid_logs:
            log = WorkoutLog(
                user_id=current_user.user_id,
                exercise_id=item['exercise_id'],
                date=chosen_date,
                sets=item['sets'],
                reps=item['reps'],
                weight=item['weight'],
                notes=item['notes']
            )
            db.session.add(log)
        db.session.commit()
        flash('Registros de entrenamiento guardados exitosamente.', 'success')
        return redirect(url_for('workout_log.history'))
    
    return render_template('workout/add_logs.html', routine_day=routine_day, exercises=exercises)

@bp.route('/<string:date_str>')
@login_required
def view_day(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        abort(400)
    
    #Obtenemos los registros del usuario en esa fecha
    logs = WorkoutLog.query.filter_by(
        user_id=current_user.user_id,
        date=date)
    
    if not logs:
        abort(404)
    
    return render_template('workout/day_detail.html', date=date, logs=logs)

@bp.route('/history')
@bp.route('/history/<int:user_id>')
@login_required
def history(user_id=None):
    if user_id is None:
        target_user = current_user
    else:
        target_user = User.query.get_or_404(user_id)
        if current_user.user_id != target_user.user_id and not current_user.is_admin:
            abort(403)

    #Filtro de fechas
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    query = WorkoutLog.query.filter_by(user_id=target_user.user_id)
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            query = query.filter(WorkoutLog.date >= start_date)
        except ValueError:
            flash("Fecha de inicio inválida", "warning")

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            query = query.filter(WorkoutLog.date <= end_date)
        except ValueError:
            flash("Fecha de fin inválida", "warning")

    logs = query.order_by(WorkoutLog.date.desc()).all()
    
    return render_template(
        'workout/history.html',
        logs=logs,
        target_user=target_user,
        start_date=start_date_str,
        end_date=end_date_str)


