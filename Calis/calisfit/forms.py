from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, IntegerField, SelectField,
                     FloatField)
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, ValidationError, NumberRange)
from calisfit.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if not User.create_db(debug=False):
            raise ValidationError(
                'Something went wrong, Please reload the Page')
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Taken!')

    def validate_email(self, email):
        User.create_db(debug=False)
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is Already Taken!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class MyBodyForm(FlaskForm):
    height = FloatField(
        "Height",
        validators=[
			InputRequired(),
            NumberRange(min=50, max=255)],
        render_kw={'placeholder': 'In CM'})
    age = IntegerField(
        "Age",
        validators=[
			InputRequired(),
            NumberRange(min=1, max=150)],
        render_kw={'placeholder': 'In Numbers'})
    weight = FloatField(
        "Weight",
        validators=[
			InputRequired(),
            NumberRange(min=1, max=300)],
        render_kw={'placeholder': 'In KGs'})
    gender = SelectField(
        'Gender',
        choices=[
                        ('M', 'Male'),
                        ('F', 'Female')
        ],
        validators=[InputRequired()]
    )
    activity_level = SelectField(
        "Activity Level",
        choices=[
            ("sedentary", "I am sedentary (little or no exercise)"),
            ("lightly", "I am lightly active (light exercise or sports 1-3 days per week)"),
            ("moderately", "I am moderately active (moderate exercise or sports 3-5 days per week)"),
            ("active", "I am very active (hard exercise or sports 6-7 days per week)"),
            ("super", "I am super active (very hard exercise or sports and a physical job)")
        ], validators=[InputRequired()]
    )
    submit = SubmitField('Submit')
