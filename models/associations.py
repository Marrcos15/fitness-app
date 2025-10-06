from app import db

# Tabla intermedia: exercise_muscle_group
exercise_muscle_group = db.Table(
    'exercise_muscle_group',
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.exercise_id'), primary_key=True),
    db.Column('muscle_group_id', db.Integer, db.ForeignKey('muscle_group.muscle_group_id'), primary_key=True)
)