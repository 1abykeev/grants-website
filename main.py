
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

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///global_grants.db"
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
        new_uni = University(
            name=form.uni_name.data,
            logo_url=form.uni_logo.data,
            picture_url=form.uni_picture.data,
            description=form.uni_desc.data,
            uni_off_page_url=form.uni_official_page_link.data,
            location=form.uni_location.data,
            language_of_education=form.language_of_education.data,
            prep_school=form.prep_school.data,
            study_programs_link=form.study_programs_link.data,
            application_deadline=form.application_deadline.data,
            application_fee=form.application_fee.data,
            tuition_fee=form.tuition_fee.data,
            tuition_fee_link=form.tuition_fee_link.data,
            requirements=form.requirements.data,
            scholarship_available=form.scholarship_available.data,
            country=form.country.data
        )
        
        # Add the new university to the database and commit the transaction
        db.session.add(new_uni)
        db.session.commit()

        # Redirect to a success page or the university list page (you can customize as needed)
        return redirect(url_for('university_list'))

    return render_template('universities.html', form=form)


#################################### Uni goes to Uni Details

@app.route('/university/<int:uni_id>')
def university_details(uni_id):
    # Query the university by ID
    university = University.query.get_or_404(uni_id)
    return render_template('university_details.html', university=university)



if __name__ == "__main__":
    app.run(debug=True)