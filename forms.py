from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, SelectMultipleField, IntegerField, FloatField,
    BooleanField
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Optional

# Importamos nuestros validadores personalizados
from utils.validators import (
    EmailValidator, PasswordValidator,
    PositiveNumberValidator, RequiredValidator
)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), EmailValidator()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


class RegisterForm(FlaskForm):
    name = StringField('Nombre', validators=[RequiredValidator(), Length(2, 100)])
    email = StringField('Email', validators=[RequiredValidator(), EmailValidator()])
    password = PasswordField(
        'Contraseña',
        validators=[PasswordValidator(min_length=8)]
    )
    password2 = PasswordField(
        'Repetir contraseña',
        validators=[EqualTo('password', message='Las contraseñas deben coincidir')]
    )
    submit = SubmitField('Registrarse')


class UserForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[RequiredValidator(), Length(2, 80)])
    email = StringField('Email', validators=[RequiredValidator(), EmailValidator()])
    password = PasswordField(
        'Nueva contraseña',
        validators=[Optional(), PasswordValidator(min_length=8)]
    )
    password2 = PasswordField(
        'Repetir nueva contraseña',
        validators=[Optional(), EqualTo('password', message='Las contraseñas deben coincidir')]
    )
    is_admin = BooleanField("Administrador")
    submit = SubmitField('Actualizar perfil')

class ExerciseForm(FlaskForm):
    name = StringField('Nombre', validators=[RequiredValidator(), Length(2, 80)])
    description = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])
    equipment_id = SelectField('Equipo', coerce=int, validators=[RequiredValidator()])
    difficulty_id = SelectField('Dificultad', coerce=int, validators=[RequiredValidator()])
    estimated_time_min = IntegerField(
        'Tiempo estimado (min)',
        validators=[Optional(), PositiveNumberValidator(allow_zero=False)]
    )
    muscle_groups = SelectMultipleField(
        'Grupos musculares',
        coerce=int,
        validators=[RequiredValidator()]
    )
    submit = SubmitField('Añadir ejercicio')

class ExerciseImportForm(FlaskForm):
    csv_file = FileField(
        'Archivo CSV',
        validators=[
            FileRequired('Debes seleccionar un archivo CSV.'),
            FileAllowed(['csv'], 'Solo se permiten archivos CSV.')
        ]
    )
    submit = SubmitField('Importar ejercicios')

class RoutineForm(FlaskForm):
    month = IntegerField('Mes', validators=[DataRequired(), NumberRange(min=1, max=12)])
    year = IntegerField('Año', validators=[DataRequired(), NumberRange(min=2020, max=2100)])
    exercises1 = SelectMultipleField('Ejercicios día 1', coerce=int, validators=[RequiredValidator()])
    exercises2 = SelectMultipleField('Ejercicios día 2', coerce=int, validators=[RequiredValidator()])
    exercises3 = SelectMultipleField('Ejercicios día 3', coerce=int, validators=[RequiredValidator()])
    exercises4 = SelectMultipleField('Ejercicios día 4', coerce=int, validators=[RequiredValidator()])
    submit = SubmitField('Añadir rutina')

class RoutineImportForm(FlaskForm):
    csv_file = FileField(
        'Archivo CSV',
        validators=[
            FileRequired('Debes seleccionar un archivo CSV.'),
            FileAllowed(['csv'], 'Solo se permiten archivos CSV.')
        ]
    )
    submit = SubmitField('Importar rutinas')

class WorkoutLogForm(FlaskForm):
    sets = IntegerField("Series", validators=[RequiredValidator(), NumberRange(min=1, max=50)])
    reps = IntegerField("Repeticiones", validators=[RequiredValidator(), NumberRange(min=1, max=200)])
    weight = FloatField("Peso (kg)", validators=[Optional(), PositiveNumberValidator(allow_zero=True)])
    duration = IntegerField("Duración (min)", validators=[Optional(), NumberRange(min=1, max=300)])
    notes = TextAreaField("Notas", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Guardar")
