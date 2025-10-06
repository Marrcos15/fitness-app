from app import db

class RoutineDay(db.Model):
    __tablename__ = 'routine_day'

    day_id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.routine_id'), nullable=False)
    name = db.Column(db.String(20), nullable=False) # AAAA-MM n

    #Relaciones
    routine = db.relationship('Routine', back_populates='days')
    exercises_assoc = db.relationship('RoutineDayExercise', back_populates='routine_day', cascade='all, delete-orphan')

    @property
    def exercises(self):
        """ Devuelve los ejercicios ordenamos por 'order' """
        return sorted(
            [assoc.exercise for assoc in self.exercises_assoc],
            key=lambda e: next(a.order for a in self.exercises_assoc if a.exercise == e)
        )