from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from utils.decorators import admin_required
from app import db
from models import Exercise, Equipment, DifficultyLevel, MuscleGroup, RoutineDayExercise
from forms import ExerciseForm, ExerciseImportForm
import csv
from io import TextIOWrapper

bp = Blueprint('exercise', __name__, url_prefix='/exercises')

@bp.route('/add', methods=['POST', 'GET'])
@login_required
@admin_required
def add_exercise():
    form = ExerciseForm()
    # Cargar opciones de los select
    form.equipment_id.choices = [(e.equipment_id, e.name) for e in Equipment.query.all()]
    form.difficulty_id.choices = [(d.difficulty_id, d.name) for d in DifficultyLevel.query.all()]
    form.muscle_groups.choices = [(m.muscle_group_id, m.name) for m in MuscleGroup.query.all()]

    if form.validate_on_submit():
        try:
            exercise = Exercise(
                name=form.name.data,
                description=form.description.data,
                equipment_id=form.equipment_id.data,
                difficulty_id=form.difficulty_id.data,
                estimated_time_min=form.estimated_time_min.data,
            )
            # Agregar grupos musculares
            exercise.muscle_groups = MuscleGroup.query.filter(
                MuscleGroup.muscle_group_id.in_(form.muscle_groups.data)
            ).all()

            db.session.add(exercise)
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                flash('Ya existe un ejercicio con ese nombre.', 'warning')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al añadir el ejercicio: {str(e)}', 'danger')
        
        flash('Ejercicio añadido correctamente', 'success')
        return redirect(url_for('exercise.add_exercise'))
    
    return render_template('exercises/form.html', form=form)

@bp.route('/', methods=['GET'])
@login_required
def view_exercises():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("q", "").strip()
    muscle_filter = request.args.get("muscle", "").strip()

    muscle_groups = MuscleGroup.query.all()
    exercises_groups = {}

    # Si hay filtro de músculo → mostrar solo ese grupo
    if muscle_filter:
        muscle = MuscleGroup.query.filter_by(name=muscle_filter).first()
        if muscle:
            query = Exercise.query

            if search_query:
                query = query.filter(Exercise.name.ilike(f"%{search_query}%"))

            query = query.join(Exercise.muscle_groups).filter(MuscleGroup.name == muscle.name)

            exercises_groups[muscle.name] = query.order_by(Exercise.name).paginate(page=page, per_page=6)

    else:
        # Mostrar todos los grupos
        for muscle in muscle_groups:
            query = Exercise.query

            if search_query:
                query = query.filter(Exercise.name.ilike(f"%{search_query}%"))

            query = query.filter(Exercise.muscle_groups.any(muscle_group_id=muscle.muscle_group_id))
            exercises_groups[muscle.name] = query.order_by(Exercise.name).paginate(page=page, per_page=6)

    return render_template(
        "exercises/list.html",
        exercises_groups=exercises_groups,
        muscle_groups=muscle_groups,
        search_query=search_query,
        muscle_filter=muscle_filter
    )


@bp.route('/<int:exercise_id>', methods=['GET'])
@login_required
def detail_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        return render_template('exercises/detail.html', exercise=exercise)
    else:
        flash('Ejercicio no encontrado', 'warning')
        return redirect(url_for('exercise.view_exercises'))
    
@bp.route('/delete/<int:exercise_id>', methods=['POST'])
@login_required
@admin_required
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    if exercise is None:
        flash('Ejercicio no encontrado', 'warning')
        return redirect(url_for('exercise.view_exercises'))
    
    # Eliminar relaciones en RoutineDayExercise antes de borrar el ejercicio
    try:
        RoutineDayExercise.query.filter_by(exercise_id=exercise_id).delete()

        db.session.delete(exercise)
        db.session.commit()
        flash('Ejercicio borrado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al borrar el ejercicio: {str(e)}', 'danger')
    
    return redirect(url_for('exercise.view_exercises'))

@bp.route('/edit/<int:exercise_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    form = ExerciseForm(obj=exercise)
    # Cargar opciones de los select
    form.equipment_id.choices = [(e.equipment_id, e.name) for e in Equipment.query.all()]
    form.difficulty_id.choices = [(d.difficulty_id, d.name) for d in DifficultyLevel.query.all()]
    form.muscle_groups.choices = [(m.muscle_group_id, m.name) for m in MuscleGroup.query.all()]

    # Preseleccionar los grupos musculares
    if request.method == 'GET':
        form.muscle_groups.data = [m.muscle_group_id for m in exercise.muscle_groups]

    if form.validate_on_submit():
        exercise.name = form.name.data
        exercise.description = form.description.data
        exercise.equipment_id = form.equipment_id.data
        exercise.difficulty_id = form.difficulty_id.data
        exercise.estimated_time_min = form.estimated_time_min.data
        exercise.muscle_groups = MuscleGroup.query.filter(
            MuscleGroup.muscle_group_id.in_(form.muscle_groups.data)
        ).all()
        db.session.commit()
        flash('Ejercicio actualizado correctamente', 'success')
        return redirect(url_for('exercise.detail_exercise', exercise_id=exercise.exercise_id))

    return render_template('exercises/form.html', form=form, edit=True)

@bp.route('/import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_exercises():
    form = ExerciseImportForm()

    if form.validate_on_submit():
        if not form.csv_file.data:
            flash("Debes seleccionar un archivo CSV.", "warning")
            return redirect(url_for('exercise.import_exercises'))

        try:
            file = TextIOWrapper(form.csv_file.data, encoding='utf-8')
            reader = csv.DictReader(file)

            imported = 0
            skipped = 0

            for row in reader:
                name = row.get("name", "").strip()
                if not name:
                    continue  # sin nombre, lo ignoramos

                # Evitar duplicados
                existing = Exercise.query.filter_by(name=name).first()
                if existing:
                    skipped += 1
                    continue

                # Buscar o crear equipo
                equipment = None
                if row.get("equipment"):
                    equipment = Equipment.query.filter_by(name=row["equipment"].strip()).first()
                    if not equipment:
                        equipment = Equipment(name=row["equipment"].strip())
                        db.session.add(equipment)
                        db.session.commit()

                # Buscar o crear dificultad
                difficulty = None
                if row.get("difficulty"):
                    difficulty = DifficultyLevel.query.filter_by(name=row["difficulty"].strip()).first()
                    if not difficulty:
                        difficulty = DifficultyLevel(name=row["difficulty"].strip())
                        db.session.add(difficulty)
                        db.session.commit()

                # Crear ejercicio
                exercise = Exercise(
                    name=name,
                    description=row.get("description", "").strip(),
                    equipment_id=equipment.equipment_id if equipment else None,
                    difficulty_id=difficulty.difficulty_id if difficulty else None,
                )
                db.session.add(exercise)
                db.session.commit()

                # Asociar grupos musculares
                muscles_raw = row.get("muscle_groups", "")
                muscles = [m.strip() for m in muscles_raw.split(",") if m.strip()]
                for m in muscles:
                    mg = MuscleGroup.query.filter_by(name=m).first()
                    if not mg:
                        mg = MuscleGroup(name=m)
                        db.session.add(mg)
                        db.session.commit()
                    exercise.muscle_groups.append(mg)
                db.session.commit()

                imported += 1

            msg = f"✅ {imported} ejercicios importados correctamente."
            if skipped > 0:
                msg += f" ⚠️ {skipped} duplicados fueron omitidos."
            flash(msg, "success")

            return redirect(url_for('exercise.view_exercises'))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al importar el archivo: {str(e)}", "danger")

    return render_template('exercises/import.html', form=form)