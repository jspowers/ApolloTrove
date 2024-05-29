import logging
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .auth import auth_bp
# from .forms.login_form import LoginForm
from apollotrove.models.user import User
from apollotrove.extensions import apollo_db


@auth_bp.route('/')
def auth_home():
    return render_template('auth.html')

@auth_bp.route('/login', methods=['POST', 'GET'])
def auth_login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('home.home_profile'))
    

    form_username = request.form.get('username')
    form_password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = apollo_db.session.execute(
        apollo_db.select(User).filter_by(username = form_username)
        ).scalar_one_or_none()
    
    if request.method == 'POST':
        if not user: 
            logging.warning('user attempted username does not exist in database.')
            error = 'No matching accounts with given username. Please try again.'
        elif check_password_hash(user.password, form_password):
            logging.info('User successfully logged into account.')
            login_user(user, remember=remember)
            return redirect(url_for('home.home_profile'))
        elif check_password_hash(user.password, form_password) == False:
            logging.warning('user attempted username/password combo does not match.')
            error = 'Invalid credentials. Please try again.'
    if error:
        flash(error)
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def auth_register():
    
    if request.method == 'GET':
        # check to see if current user is authenticated
        if current_user.is_authenticated:
            return redirect(url_for('home.home_profile'))
        return render_template('register.html') 
    
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # User Registration form validation
    errors = []
    user_email = apollo_db.session.execute(
        apollo_db.select(User).filter_by(email = email)
        ).scalar_one_or_none()
    
    user_username = apollo_db.session.execute(
        apollo_db.select(User).filter_by(username = username)
        ).scalar_one_or_none()
    
    if user_username:
        errors.append('Username already registered with another accounts.')
    if user_email:
        errors.append('Email already registered with existing accounts.')
    if password != confirm_password:
        errors.append('Passwords do not match, pease try again.')
    
    if len(errors) == 0:
        new_user = User(
            email=email,
            username=username,
            password = generate_password_hash(password, method='scrypt'),
            first_name = first_name,
            last_name = last_name,
            )
        apollo_db.session.add(new_user)
        apollo_db.session.commit()
        user = apollo_db.session.execute(
            apollo_db.select(User).filter_by(username = username)
            ).scalar_one_or_none()
        login_user(user, remember=False)
        return redirect(url_for('home.home_profile'))
    else:
        for error in errors:
            flash(error)
        return render_template('register.html')



@auth_bp.route('/logout')
def auth_logout():
    if current_user.is_authenticated:
        logout_user()
        return render_template('logout.html')
    else:
        return render_template(
            'index.html',
            current_user_authenticated = current_user.is_authenticated,
            user_username = current_user.username,
        )