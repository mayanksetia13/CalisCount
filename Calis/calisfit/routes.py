from flask import (render_template, url_for, flash,
                   redirect, request)
from calisfit import app, db, bcrypt
from calisfit.forms import (RegistrationForm, LoginForm,
                            MyBodyForm, UpdateAccountForm)
from calisfit.models import User, Cred
from flask_login import (login_user, current_user,
                         logout_user, login_required)


@app.route('/')
def index():
    db.create_all()
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
                    gender=form.gender.data,
                    email=form.email.data,
                    password=hashed_password)
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
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('about'))
            flash('Login Unsuccessful. Please check your password!', 'danger')
        else:
            flash("Login Unsuccessful. Please Check Username", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/body', methods=['GET', 'POST'])
def body():
    form = MyBodyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            track = Cred(
                user_id=current_user.id,
                height=form.height.data,
                weight=form.weight.data,
                age=form.age.data,
                activity=form.activity.data,
            )
            track.cal(gender=current_user.gender)
            db.session.add(track)
            db.session.commit()
            return redirect('track')
    return render_template('body.html', form=form)


@app.route('/learn')
def learn():
    return render_template('learn.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect('/')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = User.save_picture(app, form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Profile has been updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    # for displaying profile picture
    if 'default' in current_user.image_file:
        image_file = url_for(
            'static', filename='images/' + current_user.image_file)
    else:
        image_file = url_for(
            'static', filename='profile_pics/' + current_user.image_file)
        
    return render_template('profile.html',
                           title='Profile',
                           image_file=image_file,
                           form=form)


@app.route('/track')
@login_required
def trackrecord():

    tracks = Cred.query.order_by(
        db.desc('time')
    ).filter_by(
        user_id=current_user.id
    )

    first = tracks.first()

    path = first.display_histogram(
        id=current_user.id,
        tracks=tracks,
        app=app
    )
    return render_template('track.html',
                           title='TrackRecord',
                           path=path)
