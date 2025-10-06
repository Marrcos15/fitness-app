from app import db
from datetime import date

class WorkoutLog(db.Model):
    __tablename__ = 'workout_log'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.exercise_id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # en kg
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.CheckConstraint('sets > 0', name='ck_sets_positive'),
        db.CheckConstraint('reps > 0', name='ck_reps_positive'),
        db.CheckConstraint('weight >=0', name='ck_weight_non_negative'),
        db.Index('ix_log_user_date', 'user_id', 'date'),
    )

    # Relaciones
    user = db.relationship('User', back_populates='logs')
    exercise = db.relationship('Exercise', back_populates='logs')