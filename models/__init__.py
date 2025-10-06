# Importar modelos para que SQLAlchemy los registre
from .user import User, login_manager
from .equipment import Equipment
from .difficulty_level import DifficultyLevel
from .muscle_group import MuscleGroup
from .exercise import Exercise
from .routine import Routine
from .routine_day import RoutineDay
from .routine_day_exercise import RoutineDayExercise
from .workout_log import WorkoutLog


#Exportar los modelos
__all__ = ['User','login_manager', 'Equipment', 'DifficultyLevel', 'MuscleGroup', 'Exercise', 'Routine', 'RoutineDay', 'RoutineDayExercise', 'WorkoutLog']