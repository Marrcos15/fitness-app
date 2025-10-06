from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from utils.decorators import admin_required
from app import db
from models import Routine, Exercise, RoutineDay, RoutineDayExercise
from forms import RoutineForm, RoutineImportForm
import csv
from io import TextIOWrapper

bp = Blueprint('routine', __name__, url_prefix='/routines')
@bp.route('/add', methods=['POST', 'GET'])
@login_required
@admin_required
def add_routine():
    form = RoutineForm()
    # Cargar campos select
    exercices = Exercise.query.all()
    form.exercises1.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises2.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises3.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises4.choices = [(e.exercise_id, e.name) for e in exercices]

    if form.validate_on_submit():
        routine = Routine(
            month = form.month.data,
            year = form.year.data
        )
        db.session.add(routine)
        db.session.commit()
        flash('Rutina añadida correctamente, registrando dias de la rutina.', 'success')
        
        try:
            # Observar los días de rutina
            for n in range(1, 5):
                routine_day = RoutineDay(
                    routine_id=routine.routine_id,
                    name=f"{routine.year}-{str(routine.month).zfill(2)} {n}"
                )
                db.session.add(routine_day)
                db.session.commit()

                exercise_field = getattr(form, f'exercises{n}')
                selected_exercises = exercise_field.data

                clean_ids = list(dict.fromkeys(selected_exercises))
                for idx, exercise_id in enumerate(clean_ids, start=1):
                    routine_day_exercise = RoutineDayExercise(
                        day_id=routine_day.day_id,
                        exercise_id=exercise_id,
                        order=idx
                    )
                    db.session.add(routine_day_exercise)
                db.session.commit()


        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al añadir los días de rutina: {str(e)}', 'danger')
            return redirect(url_for('routine.add_routine'))

        flash('Rutinas diarias añadidas correctamente.', 'success')
        return redirect(url_for('routine.add_routine'))
    
    return render_template('routines/form.html', form=form)

@bp.route('/', methods=['GET'])
@login_required
def view_routines():
    routines = Routine.query.order_by(Routine.year.desc(), Routine.month.desc()).all()
    # Añadir los dias de rutina a cada rutina (sin asignar exercises)
    for routine in routines:
        routine.days = RoutineDay.query.filter_by(routine_id=routine.routine_id).all()
    return render_template('routines/list.html', routines=routines)

@bp.route('/edit/<int:routine_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_routine(routine_id):
    routine = Routine.query.get_or_404(routine_id)
    form = RoutineForm()

    # Cargar choices dinámicos
    exercices = Exercise.query.all()
    form.exercises1.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises2.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises3.choices = [(e.exercise_id, e.name) for e in exercices]
    form.exercises4.choices = [(e.exercise_id, e.name) for e in exercices]

    if form.validate_on_submit():
        routine.month = form.month.data
        routine.year = form.year.data

        # 🔹 Actualizar los días y ejercicios asociados
        try:
            for n in range(1, 5):
                routine_day = RoutineDay.query.filter_by(
                    routine_id=routine.routine_id,
                    name=f"{routine.year}-{str(routine.month).zfill(2)} {n}"
                ).first()

                if routine_day:
                    # Borramos ejercicios anteriores
                    RoutineDayExercise.query.filter_by(day_id=routine_day.day_id).delete()

                    # Añadimos los nuevos con order incremental
                    exercise_field = getattr(form, f"exercises{n}")
                    selected_exercises = exercise_field.data

                    clean_ids = list(dict.fromkeys(selected_exercises))
                    for idx, exercise_id in enumerate(clean_ids, start=1):
                        routine_day_exercise = RoutineDayExercise(
                            day_id=routine_day.day_id,
                            exercise_id=exercise_id,
                            order=idx
                        )
                        db.session.add(routine_day_exercise)

            db.session.commit()
            flash("Rutina actualizada correctamente.", "success")
            return redirect(url_for("routine.view_routines"))

        except Exception as e:
            db.session.rollback()
            flash(f"Ocurrió un error al actualizar la rutina: {str(e)}", "danger")

    else:
        # Precargar valores actuales
        form.month.data = routine.month
        form.year.data = routine.year
        for n in range(1, 5):
            routine_day = RoutineDay.query.filter_by(
                routine_id=routine.routine_id,
                name=f"{routine.year}-{str(routine.month).zfill(2)} {n}"
            ).first()
            if routine_day:
                exercise_field = getattr(form, f"exercises{n}")
                exercise_field.data = [re.exercise_id for re in routine_day.exercises]

    return render_template("routines/edit.html", form=form, routine=routine)

@bp.route('/import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_routines():
    form = RoutineImportForm()

    if form.validate_on_submit():
        file = form.csv_file.data

        try:
            file_stream = TextIOWrapper(file, encoding='utf-8')
            reader = csv.DictReader(file_stream)

            imported, skipped = 0, 0

            for row in reader:
                month = row.get('month')
                year = row.get('year')
                day_name = row.get('day_name')
                exercise_names = row.get('exercise_names')

                if not (month and year and day_name and exercise_names):
                    skipped += 1
                    continue

                # Verificar si la rutina ya existe
                routine = Routine.query.filter_by(month=month, year=year).first()
                if not routine:
                    routine = Routine(month=month, year=year)
                    db.session.add(routine)
                    db.session.commit()

                # Crear día de rutina
                routine_day = RoutineDay(routine_id=routine.routine_id, name=day_name)
                db.session.add(routine_day)
                db.session.commit()

                # Añadir ejercicios (si existen)
                exercises = [name.strip() for name in exercise_names.split('|') if name.strip()]
                for idx, ex_name in enumerate(exercises, start=1):
                    exercise = Exercise.query.filter_by(name=ex_name).first()
                    if exercise:
                        link = RoutineDayExercise(
                            day_id=routine_day.day_id,
                            exercise_id=exercise.exercise_id,
                            order=idx
                        )
                        db.session.add(link)
                db.session.commit()

                imported += 1

            flash(f"✅ {imported} rutinas importadas correctamente. ⚠️ {skipped} filas incompletas omitidas.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al importar rutinas: {str(e)}", "danger")

        return redirect(url_for('routine.view_routines'))

    return render_template('routines/import.html', form=form)