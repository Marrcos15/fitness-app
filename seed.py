# seed.py
from app import create_app, db
from models import *
from datetime import date

app = create_app()
with app.app_context():
    # Limpiar (opcional)
    db.drop_all()
    db.create_all()

    # 1. Catálogos
    equip_dumbbells = Equipment(name="Mancuernas")
    equip_bodyweight = Equipment(name="Peso corporal")
    db.session.add_all([equip_dumbbells, equip_bodyweight])

    diff_beginner = DifficultyLevel(name="Principiante")
    diff_intermediate = DifficultyLevel(name="Intermedio")
    db.session.add_all([diff_beginner, diff_intermediate])

    mg_chest = MuscleGroup(name="Pecho")
    mg_triceps = MuscleGroup(name="Tríceps")
    mg_legs = MuscleGroup(name="Piernas")
    db.session.add_all([mg_chest, mg_triceps, mg_legs])

    db.session.commit()

    # 2. Usuarios
    user1 = User(username="Example", email="correo@example.com", is_admin=True)
    user1.set_password("123456")
    db.session.add(user1)
    db.session.commit()

    # 3. Ejercicios
    pushup = Exercise(
        name="Flexiones",
        description="Flexiones clásicas de pecho",
        equipment_id=equip_bodyweight.equipment_id,
        difficulty_id=diff_beginner.difficulty_id,
        estimated_time_min=5
    )
    pushup.muscle_groups = [mg_chest, mg_triceps]

    squat = Exercise(
        name="Sentadilla",
        description="Sentadilla con peso corporal",
        equipment_id=equip_bodyweight.equipment_id,
        difficulty_id=diff_beginner.difficulty_id,
        estimated_time_min=4
    )
    squat.muscle_groups = [mg_legs]

    db.session.add_all([pushup, squat])
    db.session.commit()

    # 4. Rutina (Enero 2025)
    routine = Routine(month=1, year=2025)
    db.session.add(routine)
    db.session.commit()

    day_a = RoutineDay(routine_id=routine.routine_id, name="Día A")
    db.session.add(day_a)
    db.session.commit()

    # Asignar ejercicios al día
    assoc1 = RoutineDayExercise(day_id=day_a.day_id, exercise_id=pushup.exercise_id, order=1)
    assoc2 = RoutineDayExercise(day_id=day_a.day_id, exercise_id=squat.exercise_id, order=2)
    db.session.add_all([assoc1, assoc2])

    # 5. Logs de entrenamiento
    log1 = WorkoutLog(
        user_id=user1.user_id,
        exercise_id=pushup.exercise_id,
        date=date(2025, 1, 10),
        sets=3,
        reps=12,
        weight=0.0,
        notes="Bien, pero fatigada al final"
    )
    db.session.add(log1)

    db.session.commit()
    print("Datos de prueba cargados.")