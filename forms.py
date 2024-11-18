from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, URLField, TextAreaField, DecimalField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, Email, Regexp, Optional
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


class AddUniversityForm(FlaskForm):
    uni_name = StringField("University Name", validators=[DataRequired()])
    uni_logo = StringField("Logo PNG Link", validators=[Optional()])
    uni_picture = StringField("University Picture Link", validators=[Optional()])
    uni_desc = TextAreaField("Description", validators=[DataRequired()], render_kw={"rows": 50, "cols": 150})
    uni_official_page_link = URLField("Link to Official Webpage of University", validators=[Optional()])
    uni_location = StringField("Location", validators=[DataRequired()])
    language_of_education = StringField("Language of Education", validators=[Optional()])
    prep_school = StringField("Has Prep School", validators=[Optional()])  # Changed to StringField
    study_programs_link = URLField("Link to All Study Programs", validators=[Optional()])
    application_deadline = StringField("Application Deadline", validators=[Optional()])
    application_fee = StringField("Application Fee", validators=[Optional()])  # Changed to StringField
    tuition_fee = TextAreaField("Tuition Fee", validators=[DataRequired()], render_kw={"rows": 30, "cols": 80})
    # tuition_fee = StringField("Tuition Fee", validators=[Optional()])
    tuition_fee_link = URLField("Link to Tuition Fees", validators=[Optional()])
    requirements = TextAreaField("Requirements", validators=[Optional()], render_kw={"rows": 30, "cols": 80})
    scholarship_available = TextAreaField("Scholarshi", validators=[Optional()], render_kw={"rows": 30, "cols": 80})
    #scholarship_available = StringField("Scholarship Available", validators=[Optional()])  # Changed to StringField
    country = SelectField("Country", choices=[('Poland', 'Poland'), ('Turkey', 'Turkey')], validators=[DataRequired()])