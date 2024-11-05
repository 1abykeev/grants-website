from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, Email, Regexp
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
    course_code = StringField(
        "Course Code",
        validators=[
            DataRequired(),
            Regexp(r'^\d{6}$', message="Please enter a valid 6-digit course code.")
        ]
    )
    submit = SubmitField("Login")