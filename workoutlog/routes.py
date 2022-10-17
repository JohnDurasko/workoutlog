from time import strptime
from workoutlog import app, db, bcrypt
from datetime import datetime
from flask import render_template, url_for, redirect, request, abort
from workoutlog.models import User, Workout, Exercise
from workoutlog.forms import NewExercise, NewWorkout, SignUp, Login, SearchWorkout
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
  if current_user.is_authenticated:
    workouts = Workout.query.filter_by(author=current_user).all()
    total = len(workouts)
    return render_template("index.html", workouts=workouts, total=total)
  return render_template("index.html")

@app.route('/my_workouts', methods=['GET', 'POST'])
@login_required
def my_workouts():
  form = SearchWorkout()
  if form.validate_on_submit():
    return redirect(url_for('workouts_date', date=form.date.data.strftime('%Y%m%d')))
  elif request.method == 'GET':
    form.date.data = datetime.now()
  workouts = Workout.query.filter_by(author=current_user).all()
  workouts = Workout.query.filter_by(author=current_user).order_by(Workout.date).all()
  return render_template("my_workouts.html", form=form, workouts=reversed(workouts))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUp()
  if form.validate_on_submit():
    hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.user.data, password=hashed_pass)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = Login()
  if form.validate_on_submit():
      user = User.query.filter_by(username=form.user.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        return redirect(url_for('my_workouts'))
  return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/workouts/<int:workout_id>/update', methods=['GET', 'POST'])
@login_required
def update_workout(workout_id):
  workout = Workout.query.get_or_404(workout_id) 
  form = NewExercise()
  if form.validate_on_submit():
    exercise = Exercise(name=form.exercise.data, sets=form.sets.data, reps=form.reps.data, weight=form.weight.data, exercises=workout)
    db.session.add(exercise)
    db.session.commit()
    return redirect(url_for('update_workout', workout_id=workout.id))
  return render_template('update_workout.html', workout=workout, form=form)

@app.route('/new_workout', methods=['GET', 'POST'])
@login_required
def new_workout():
  form = NewWorkout()
  if form.validate_on_submit():
    workout = Workout(author=current_user, date=form.date.data)
    db.session.add(workout)
    db.session.commit()
    return redirect(url_for('update_workout', workout_id=workout.id))
  elif request.method == 'GET':
    form.date.data = datetime.now()
  return render_template('new_workout.html', form=form)

@app.route("/workouts/<int:workout_id>")
@login_required
def workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return render_template('workout.html', workout=workout)

@app.route("/workout/<int:workout_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.author != current_user:
        abort(403)
    for exercise in workout.exercises:
      db.session.delete(exercise)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('my_workouts'))

@app.route("/exercise/<int:exercise_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_exercise(exercise_id):
  exercise = Exercise.query.get_or_404(exercise_id)
  db.session.delete(exercise)
  db.session.commit()
  return redirect(url_for('update_workout', workout_id=exercise.workout_id))

@app.route('/my_workouts/<string:date>')
@login_required
def workouts_date(date):
  d = datetime(int(date[:4]), int(date[4:6]), int(date[6:]), 0, 0, 0)
  workouts = Workout.query.filter_by(author=current_user, date=d).all()
  return render_template("workouts_date.html", workouts=workouts)