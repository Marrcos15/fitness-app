from app import db
from .associations import exercise_muscle_group

class MuscleGroup(db.Model):
    __tablename__ = 'muscle_group'
    muscle_group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    exercises = db.relationship(
        'Exercise',
        secondary=exercise_muscle_group,
        back_populates='muscle_groups'
    )