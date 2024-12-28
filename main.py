
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin
from forms import RegisterForm, LoginForm, AddUniversityForm
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, login_user, current_user, logout_user
from functools import wraps
from flask import abort
from database import db, User, Base, University
from markupsafe import Markup
import bleach
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "postgresql://aktan:YmPRml5A83t25KNsaxAW2kZrsNYXFBJJ@dpg-cto0ibdsvqrc73b4vvg0-a/gg_postgresql")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///global_grants.db")
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

db.init_app(app)

    


with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash("You need to be logged in to access this course.")
            return abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function






# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function



# Define the custom nl2br filter
@app.template_filter('nl2br')
def nl2br_filter(value):
    return Markup(value.replace("\n", "<br>"))





@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        #This line will authenticate the user with Flask-Login
        login_user(new_user)

        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

        if user and check_password_hash(user.password, password):
            login_user(user)
            if form.course_code.data == "240190":
                return redirect(url_for('turkiye' ))
            elif form.course_code.data == "240236":
                return redirect(url_for('hungary'))
            elif form.course_code.data == "240290":
                return redirect(url_for('tb_basic'))
            elif form.course_code.data == "250303":
                return redirect(url_for('dashboard'))
            else:
                # Set an error message for invalid course code
                form.course_code.errors.append("Invalid course code. Please enter a valid course code.")
            #return redirect(url_for('pricing'))

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

@app.route('/course/turkiye')
@login_required
def turkiye():
    return render_template("turkiye.html")

@app.route('/course/hungary')
@login_required
def hungary():
    return render_template("hungary.html")

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/turkiye-desc')
def turkiye_desc():
    return render_template("turkiye_desc.html")

@app.route('/poland-desc')
def poland_desc():
    return render_template("poland_desc.html")

@app.route('/turkiye-direct-application')
def turkiye_direct():
    return render_template("turkiye_direct.html")


@app.route('/hungary-desc')
def hungary_desc():
    return render_template("hungary_desc.html")

# @app.route('/poland-unis')
# def poland_unis():
#     return render_template("poland_unis.html")

# @app.route('/university-details')
# def university_details():
#     return render_template("university_details.html")


# for admin only
@app.route('/university-list', methods=['GET', 'POST'])
def university_list():
    universities = University.query.all()  # Query to get all universities
    return render_template('universities.html', universities=universities)

@app.route('/university-list-poland', methods=['GET', 'POST'])
def university_list_poland():
    universities = University.query.filter_by(country='Poland').all()  
    return render_template('universities.html', universities=universities)

@app.route('/university-list-turkiye', methods=['GET', 'POST'])
def university_list_turkiye():
    universities = University.query.filter_by(country='Turkey').all()  
    return render_template('universities.html', universities=universities)


@app.route('/add-university-page', methods=['GET', 'POST'])
def add_university_page():
    form = AddUniversityForm() 
    return render_template('add_university.html', form=form)


@app.route('/add-university', methods=['GET', 'POST'])
def add_university():
    form = AddUniversityForm()
    if form.validate_on_submit():

        # Define the allowed tags globally
        allowed_tags = ['strong', 'em', 'u', 'p', 'b', 'i']

        # Sanitize each form field, allowing specific tags
        sanitized_uni_name = bleach.clean(form.uni_name.data, tags=allowed_tags, attributes={})
        sanitized_uni_logo = bleach.clean(form.uni_logo.data, tags=allowed_tags, attributes={})
        sanitized_uni_picture = bleach.clean(form.uni_picture.data, tags=allowed_tags, attributes={})
        sanitized_description = bleach.clean(form.uni_desc.data, tags=allowed_tags, attributes={})
        sanitized_off_page_url = bleach.clean(form.uni_official_page_link.data, tags=allowed_tags, attributes={})
        sanitized_location = bleach.clean(form.uni_location.data, tags=allowed_tags, attributes={})
        sanitized_language_of_education = bleach.clean(form.language_of_education.data, tags=allowed_tags, attributes={})
        sanitized_prep_school = bleach.clean(form.prep_school.data, tags=allowed_tags, attributes={})
        sanitized_study_programs_link = bleach.clean(form.study_programs_link.data, tags=allowed_tags, attributes={})
        sanitized_application_deadline = bleach.clean(form.application_deadline.data, tags=allowed_tags, attributes={})
        sanitized_application_fee = bleach.clean(form.application_fee.data, tags=allowed_tags, attributes={})
        sanitized_tuition_fee = bleach.clean(form.tuition_fee.data, tags=allowed_tags, attributes={})
        sanitized_tuition_fee_link = bleach.clean(form.tuition_fee_link.data, tags=allowed_tags, attributes={})
        sanitized_requirements = bleach.clean(form.requirements.data, tags=allowed_tags, attributes={})
        sanitized_scholarship_available = bleach.clean(form.scholarship_available.data, tags=allowed_tags, attributes={})
        sanitized_country = bleach.clean(form.country.data, tags=allowed_tags, attributes={})

        # Create a new university object using the sanitized data
        new_uni = University(
            name=sanitized_uni_name,
            logo_url=sanitized_uni_logo,
            picture_url=sanitized_uni_picture,
            description=sanitized_description,
            uni_off_page_url=sanitized_off_page_url,
            location=sanitized_location,
            language_of_education=sanitized_language_of_education,
            prep_school=sanitized_prep_school,
            study_programs_link=sanitized_study_programs_link,
            application_deadline=sanitized_application_deadline,
            application_fee=sanitized_application_fee,
            tuition_fee=sanitized_tuition_fee,
            tuition_fee_link=sanitized_tuition_fee_link,
            requirements=sanitized_requirements,
            scholarship_available=sanitized_scholarship_available,
            country=sanitized_country
        )

        # Add the new university to the database and commit the transaction
        db.session.add(new_uni)
        db.session.commit()

        # Redirect to a success page or the university list page
        return redirect(url_for('university_list'))

    return render_template('universities.html', form=form)



# Use a decorator so only an admin user can edit a university
@app.route("/edit-university/<int:university_id>", methods=["GET", "POST"])
def edit_university(university_id):
    # Fetch the university record or return a 404 error if not found
    university = db.get_or_404(University, university_id)
    
    # Pre-populate the form with the existing university data
    edit_form = AddUniversityForm(
        uni_name=university.name,
        uni_logo=university.logo_url,
        uni_picture=university.picture_url,
        uni_desc=university.description,
        uni_official_page_link=university.uni_off_page_url,
        uni_location=university.location,
        language_of_education=university.language_of_education,
        prep_school=university.prep_school,
        study_programs_link=university.study_programs_link,
        application_deadline=university.application_deadline,
        application_fee=university.application_fee,
        tuition_fee=university.tuition_fee,
        tuition_fee_link=university.tuition_fee_link,
        requirements=university.requirements,
        scholarship_available=university.scholarship_available,
        country=university.country
    )
    
    # Define allowed HTML tags for sanitization
    allowed_tags = ['strong', 'em', 'u', 'p', 'b', 'i']

    # Process the form submission
    if edit_form.validate_on_submit():
        # Sanitize each form field to allow only the specified HTML tags
        sanitized_uni_name = bleach.clean(edit_form.uni_name.data, tags=allowed_tags, attributes={})
        sanitized_uni_logo = bleach.clean(edit_form.uni_logo.data, tags=allowed_tags, attributes={})
        sanitized_uni_picture = bleach.clean(edit_form.uni_picture.data, tags=allowed_tags, attributes={})
        sanitized_description = bleach.clean(edit_form.uni_desc.data, tags=allowed_tags, attributes={})
        sanitized_off_page_url = bleach.clean(edit_form.uni_official_page_link.data, tags=allowed_tags, attributes={})
        sanitized_location = bleach.clean(edit_form.uni_location.data, tags=allowed_tags, attributes={})
        sanitized_language_of_education = bleach.clean(edit_form.language_of_education.data, tags=allowed_tags, attributes={})
        sanitized_prep_school = bleach.clean(edit_form.prep_school.data, tags=allowed_tags, attributes={})
        sanitized_study_programs_link = bleach.clean(edit_form.study_programs_link.data, tags=allowed_tags, attributes={})
        sanitized_application_deadline = bleach.clean(edit_form.application_deadline.data, tags=allowed_tags, attributes={})
        sanitized_application_fee = bleach.clean(edit_form.application_fee.data, tags=allowed_tags, attributes={})
        sanitized_tuition_fee = bleach.clean(edit_form.tuition_fee.data, tags=allowed_tags, attributes={})
        sanitized_tuition_fee_link = bleach.clean(edit_form.tuition_fee_link.data, tags=allowed_tags, attributes={})
        sanitized_requirements = bleach.clean(edit_form.requirements.data, tags=allowed_tags, attributes={})
        sanitized_scholarship_available = bleach.clean(edit_form.scholarship_available.data, tags=allowed_tags, attributes={})
        sanitized_country = bleach.clean(edit_form.country.data, tags=allowed_tags, attributes={})

        # Update the university object with new sanitized data
        university.name = sanitized_uni_name
        university.logo_url = sanitized_uni_logo
        university.picture_url = sanitized_uni_picture
        university.description = sanitized_description
        university.uni_off_page_url = sanitized_off_page_url
        university.location = sanitized_location
        university.language_of_education = sanitized_language_of_education
        university.prep_school = sanitized_prep_school
        university.study_programs_link = sanitized_study_programs_link
        university.application_deadline = sanitized_application_deadline
        university.application_fee = sanitized_application_fee
        university.tuition_fee = sanitized_tuition_fee
        university.tuition_fee_link = sanitized_tuition_fee_link
        university.requirements = sanitized_requirements
        university.scholarship_available = sanitized_scholarship_available
        university.country = sanitized_country
        
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to a success page or university list
        return redirect(url_for('university_list', university_id=university_id))
    
    # Render the form for editing
    return render_template('add_university.html', form=edit_form, is_edit=True)











# Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:uni_id>", methods=['POST'])
@admin_only
def delete_uni(uni_id):
    uni_to_delete = db.get_or_404(University, uni_id)
    db.session.delete(uni_to_delete)
    db.session.commit()
    return redirect(url_for('university_list'))



#################################### Uni goes to Uni Details

@app.route('/university/<int:uni_id>')
def university_details(uni_id):
    # Query the university by ID
    university = University.query.get_or_404(uni_id)
    return render_template('university_details.html', university=university)



##################################### COURSES 

@app.route('/course/tb-basic', methods=['GET', 'POST'])
def tb_basic():
    return render_template("tb_basic.html")
        







if __name__ == "__main__":
    app.run(debug=True)