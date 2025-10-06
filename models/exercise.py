from app import db
from .associations import exercise_muscle_group

class Exercise(db.Model):
    __tablename__ = 'exercise'

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.equipment_id'))
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulty_level.difficulty_id'))
    estimated_time_min = db.Column(db.Integer)

    # Constraints
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_exercise_name'),
    )
    
    #Relaciones
    equipment = db.relationship('Equipment', back_populates='exercises')
    difficulty = db.relationship('DifficultyLevel', back_populates='exercises')
    muscle_groups = db.relationship(
        'MuscleGroup', 
        secondary=exercise_muscle_group, 
        back_populates='exercises')
    logs = db.relationship('WorkoutLog', back_populates='exercise', cascade='all, delete-orphan')
    routine_day_exercises = db.relationship('RoutineDayExercise', back_populates='exercise')

