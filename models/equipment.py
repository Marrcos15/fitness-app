from app import db

class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    exercises = db.relationship('Exercise', back_populates='equipment')