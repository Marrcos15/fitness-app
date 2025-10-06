from app import db

class RoutineDayExercise(db.Model):
    __tablename__ = 'routine_day_exercise'
    day_id = db.Column(db.Integer, db.ForeignKey('routine_day.day_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), primary_key=True)
    order = db.Column(db.Integer, nullable=False)

    __table_args__=(
        db.UniqueConstraint('day_id', 'order', name='uq_day_order'),
    )

    # Relaciones
    routine_day = db.relationship('RoutineDay', back_populates='exercises_assoc')
    exercise = db.relationship('Exercise', back_populates='routine_day_exercises')