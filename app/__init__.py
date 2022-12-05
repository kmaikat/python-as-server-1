from flask import Flask, render_template, redirect
from .forms import SimpleForm
from .models import db, SimplePerson
from app.config import Configuration
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
Migrate(app, db)


@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/simple-form")
def simple_form_get():
    form = SimpleForm()
    return render_template("simple_form.html", form=form)

@app.route("/simple-form", methods=["POST"])
def simple_form_post():
    form = SimpleForm()

    if form.validate_on_submit():
        new_person = SimplePerson(
            name = form.data['name'],
            age = form.data['age'],
            bio = form.data['bio']
        )
        print(new_person)
        db.session.add(new_person)
        db.session.commit()
        return redirect("/")

    if form.errors:
        return "Bad Data"

@app.route("/simple-form-data")
def simple_form_data_get():
    people = SimplePerson.query.filter(SimplePerson.name.like("M%")).all()
    return render_template("simple_form_data.html", people=people)
