from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField



# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format.")])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format.")])
    password = PasswordField("Password", validators=[DataRequired()])
    course_code = IntegerField("Course Code", validators=[DataRequired()])  
    submit = SubmitField("Login")