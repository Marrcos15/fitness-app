from app import db

class DifficultyLevel(db.Model):
    __tablename__ = 'difficulty_level'
    difficulty_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    exercises = db.relationship('Exercise', back_populates='difficulty')