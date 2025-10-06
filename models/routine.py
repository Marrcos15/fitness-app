from app import db
from datetime import datetime

class Routine(db.Model):
    __tablename__ = 'routine'

    routine_id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Restrinciones
    __table_args__ = (db.UniqueConstraint('year', 'month', name='uq_routine_year_month'),)

    #Relaciones
    days = db.relationship('RoutineDay', back_populates='routine', cascade='all, delete-orphan')
