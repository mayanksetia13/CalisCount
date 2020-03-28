from flask import render_template, url_for, flash, redirect
from calisfit import app, db, bcrypt
from calisfit.forms import RegistrationForm, LoginForm
from calisfit.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!You are ready to workout', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('about'))
            flash('Login Unsuccessful. Please check your password!','danger')
        else:
            flash("Login Unsuccessful. Please Check Username", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/body')
def body():
    return render_template('body.html')


@app.route('/learn')
def learn():
    return render_template('learn.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect('/')

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html',title='Profile')

@app.route('/track')
@login_required
def trackrecord():
	return render_template('track.html',title='TrackRecord')	

