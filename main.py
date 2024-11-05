
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, login_user, current_user, logout_user
from functools import wraps
from flask import abort


app = Flask(__name__)
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///global_grants.db"
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

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

if __name__ == "__main__":
    app.run(debug=True)