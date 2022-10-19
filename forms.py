from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from workoutlog.models import User

class SignUp(FlaskForm):
  user = StringField('User', validators=[DataRequired(), Length(max=25)])
  #email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=25)])
  confirmpass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_user(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('User Exists')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Email Exists')

class Login(FlaskForm):
  user = StringField('User', validators=[DataRequired(), Length(max=25)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class NewExercise(FlaskForm):
  exercise = StringField('Exercise', validators=[DataRequired()])
  sets = IntegerField('Sets', validators=[DataRequired()])
  reps = IntegerField('Reps', validators=[DataRequired()])
  weight = IntegerField('Weight', validators=[DataRequired()])
  submit = SubmitField('Add Exercise')

class NewWorkout(FlaskForm):
  date = DateField('Workout Date', format='%Y-%m-%d', validators=[DataRequired()])
  submit = SubmitField('Add Workout')

class SearchWorkout(FlaskForm):
  date = DateField('Date Lookup', format='%Y-%m-%d', validators=[DataRequired()])
  submit = SubmitField('Search')