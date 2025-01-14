



# database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_login import UserMixin





# Define a base class for models
class Base(DeclarativeBase):
    pass

# Initialize the SQLAlchemy object, but don't call init_app here
db = SQLAlchemy(model_class=Base)

# Define the User model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))




# class University(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(10000), nullable=False)  # Changed to match form field `uni_name`
#     logo_url = db.Column(db.String(10000), nullable=True)  # Changed to match form field `uni_logo`
#     picture_url = db.Column(db.String(10000), nullable=True)  # Changed to match form field `uni_picture`
#     description = db.Column(db.Text, nullable=False)  # Changed to match form field `uni_desc`
#     uni_off_page_url = db.Column(db.String(10000), nullable=True)  # Changed to match form field `uni_official_page_link`
#     location = db.Column(db.String(10000), nullable=False)  # Changed to match form field `uni_location`
#     language_of_education = db.Column(db.String(10000), nullable=True)  # Changed to match form field `language_of_education`
#     prep_school = db.Column(db.String(10000), nullable=True)  # Changed to match form field `prep_school`
#     study_programs_link = db.Column(db.String(10000), nullable=True)  # Changed to match form field `study_programs_link`
#     application_deadline = db.Column(db.String(10000), nullable=True)  # Changed to match form field `application_deadline`
#     application_fee = db.Column(db.String(10000), nullable=True)  # Changed to match form field `application_fee`
#     tuition_fee = db.Column(db.String(10000), nullable=True)  # Changed to match form field `tuition_fee`
#     tuition_fee_link = db.Column(db.String(10000), nullable=True)  # Changed to match form field `tuition_fee_link`
#     requirements = db.Column(db.Text, nullable=True)  # Changed to match form field `requirements`
#     scholarship_available = db.Column(db.String(10000), nullable=True)  # Changed to match form field `scholarship_available`
#     country = db.Column(db.String(1000), nullable=False)  # Changed to match form field `country`

    
class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)  # Changed to Text for long names
    logo_url = db.Column(db.String(2083), nullable=True)  # Updated for URL max length
    picture_url = db.Column(db.String(2083), nullable=True)  # Updated for URL max length
    description = db.Column(db.Text, nullable=False)  # Kept as Text for long descriptions
    uni_off_page_url = db.Column(db.String(2083), nullable=True)  # Updated for URL max length
    location = db.Column(db.Text, nullable=False)  # Changed to Text for long locations
    language_of_education = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    prep_school = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    study_programs_link = db.Column(db.String(2083), nullable=True)  # Updated for URL max length
    application_deadline = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    application_fee = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    tuition_fee = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    tuition_fee_link = db.Column(db.String(2083), nullable=True)  # Updated for URL max length
    requirements = db.Column(db.Text, nullable=True)  # Kept as Text for long descriptions
    scholarship_available = db.Column(db.Text, nullable=True)  # Changed to Text for long strings
    country = db.Column(db.Text, nullable=False)  # Changed to Text for long country names

