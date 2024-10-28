
from flask import Flask, render_template, url_for, redirect, request  
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin
from forms import RegisterForm
from werkzeug.security import generate_password_hash
import secrets
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
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



@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
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
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


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

@app.route('/login')
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)