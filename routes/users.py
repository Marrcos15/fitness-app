from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from utils.decorators import admin_required
from app import db
from models import User
from forms import UserForm


bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/profile', methods=['GET'])
@bp.route('/profile/<int:user_id>')
@login_required
def user_profile(user_id=None):
    if user_id is None:
        user = User.query.get(current_user.user_id)
    else:
        user = User.query.get_or_404(user_id)
        # Verificación de permisos: Si no es admin y quiere ver otro perfil -> prohibido
        if current_user.user_id != user.user_id and not current_user.is_admin:
            abort(403)

    return render_template('users/profile.html', user=user)

@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    # Obtener el usuario a editar
    user = User.query.get_or_404(user_id)

    # Verificación de permisos:
    # - Si no es admin y no es el mismo usuario → prohibido
    if current_user.user_id != user.user_id and not current_user.is_admin:
        abort(403)  # redirige a página 403 personalizada

    form = UserForm(obj=user)
    
    # Mostrar campo para administradores
    if current_user.is_admin:
        form.is_admin.data = user.is_admin

    if form.validate_on_submit():
        # Validar que el email no esté en uso por otro usuario
        if form.email.data != user.email:
            exists = User.query.filter_by(email=form.email.data).first()
        
        if exists:
            flash("Ese email ya está en uso.", "danger")
            return render_template('users/edit.html', form=form, user=user)
    
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)

        if current_user.is_admin:
            user.is_admin = form.is_admin.data

        try:
            db.session.commit()
            flash('Perfil actualizado correctamente.', 'success')
            return redirect(url_for('user.user_profile', user_id=user.user_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al actualizar el perfil: {str(e)}', 'danger')

    return render_template('users/edit.html', user=user, form=form)

@bp.route('/list', methods=['GET'])
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@bp.route('delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.user_id == current_user.user_id:
        flash('No puedes eliminar tu propio usuario.', 'warning')
        return redirect(url_for('user.list_users'))
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Usuario eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ocurrió un error al eliminar el usuario: {str(e)}', 'danger')
    
    return redirect(url_for('user.list_users'))
