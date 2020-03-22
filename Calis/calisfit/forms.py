from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField, SubmitField , BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from calisfit.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired() , Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit= SubmitField('Register')

	def validate_username(self, username):
		if not User.create_db(debug=False):
			raise ValidationError('Something went wrong, Please reload the Page')
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username Already Taken!')

	def validate_email(self, email):
		User.create_db(debug=False)
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is Already Taken!')		


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired() , Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit= SubmitField('Login')	


