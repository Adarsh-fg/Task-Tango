from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_migrate import Migrate
from flask import jsonify
from forms import TaskForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

from forms import TaskForm 
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)  # 👈 New column
    priority = db.Column(db.String(10), nullable=False, default="Medium")  # 👈 New column

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    sort_by = request.args.get("sort_by", "default")  # Get sorting parameter from the dropdown

    query = Task.query.filter_by(user_id=current_user.id)

    if sort_by == "priority":
        query = query.order_by(
            db.case(
                (Task.priority == "High", 1),
                (Task.priority == "Medium", 2),
                (Task.priority == "Low", 3),
                else_=4,
            )
        )
    elif sort_by == "due_date":
        query = query.order_by(Task.due_date.asc())
    elif sort_by == "completed":
        query = query.order_by(Task.completed.asc())  # Sorts uncompleted tasks first
    else:
        query = query.order_by(Task.id.asc())  # Default sorting (by creation order)

    tasks = query.all()
    return render_template("index.html", tasks=tasks, form=TaskForm(), sort_by=sort_by)




@app.route("/add", methods=["POST"])
@login_required
def add_task():
    form = TaskForm()
    print("📩 Received form data:", request.form)  # Debugging print
    
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        print("✅ Task successfully added:", new_task)
        return redirect(url_for("index"))
    
    print("❌ Form submission failed:", form.errors)  # Debugging print
    return render_template("index.html", form=form, tasks=Task.query.all())



@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))


@app.route("/toggle_task/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 403

@app.route("/reorder_tasks", methods=["POST"])
@login_required
def reorder_tasks():
    data = request.get_json()
    for index, task_id in enumerate(data["order"]):
        task = Task.query.get(task_id)
        if task and task.user_id == current_user.id:
            task.order = index  # Assuming you added an 'order' column to Task model
    db.session.commit()
    return jsonify({"message": "Task order updated"})

from flask import jsonify

@app.route("/analytics")
@login_required
def analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks

    # Priority Breakdown
    priority_counts = {
        "Low": sum(1 for task in tasks if task.priority == "Low"),
        "Medium": sum(1 for task in tasks if task.priority == "Medium"),
        "High": sum(1 for task in tasks if task.priority == "High"),
    }

    return jsonify({
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "priority_counts": priority_counts
    })

@app.route("/analytics_page")
@login_required
def analytics_page():
    return render_template("analytics.html")

@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure the task belongs to the logged-in user
    if task.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("index"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")

    return redirect(url_for("index"))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
