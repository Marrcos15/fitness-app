from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from app import db
from forms import LoginForm, RegisterForm
from models import User
from utils.decorators import limiter

bp = Blueprint('auth', __name__, url_prefix='/auth')
def is_safe_url(target):
    # Previene open redirects (asegura que el dominio sea el mismo)
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Limitar a 5 intentos de login por minuto
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Email o contraseña incorrecta', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash(f'Bienvenido, {user.username}!', 'success')

        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar si el email ya existe
        if User.query.filter_by(email=form.email.data).first():
            flash('Este email ya está registrado', 'warning')
            return redirect(url_for('auth.register'))
        user = User(username=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))