from workoutlog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25), unique=True, nullable=False)
  password = db.Column(db.String(25), nullable=False)
  workouts = db.relationship('Workout', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  exercises = db.relationship('Exercise', backref='exercises', lazy=True)

  def __repr__(self):
    return f"Workout('{self.user_id}', '{self.date}', '{self.exercises}')"

class Exercise(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  sets = db.Column(db.Integer, nullable=False)
  reps = db.Column(db.Integer, nullable=False)
  weight = db.Column(db.Integer, nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

  def __repr__(self):
    return f"Exercise('{self.id}', '{self.name}', '{self.reps}', '{self.sets}', '{self.weight}')"