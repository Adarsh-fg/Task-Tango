from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField("Task Title", validators=[DataRequired()])
    due_date = DateField("Due Date", format="%Y-%m-%d", validators=[])
    priority = SelectField("Priority", choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], validators=[DataRequired()])
    submit = SubmitField("Add Task")
