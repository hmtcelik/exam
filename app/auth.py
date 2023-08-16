from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        # check user
        user = User.query.filter_by(nickname=nickname).first() 

        if not user:
            flash('Bu Takma Ad kayıtlı değil.', 'error')
            return redirect(url_for('auth.login'))
        
        if not check_password_hash(user.password, password):
            flash('Şifre yanlış.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        password_again = request.form.get('password-again')

        # check user
        user = User.query.filter_by(email=email).first() 

        if user:
            flash('Bu E-posta zaten kullanımda.', 'error')
            return redirect(url_for('auth.signup'))
        
        user = User.query.filter_by(nickname=nickname).first() 

        if user:
            flash('Bu Takma Ad zaten kullanımda.', 'error')
            return redirect(url_for('auth.signup'))
        
        if password != password_again:
            flash('Şifreler eşleşmiyor.', 'error')
            return redirect(url_for('auth.signup'))

        if len(password) < 8:
            flash('Şifre en az 8 karakterden oluşmalıdır.', 'error')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, nickname=nickname, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Hesabınız oluşturuldu.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
