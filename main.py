
from flask import Flask, render_template, url_for

app = Flask(__name__)






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