"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

db.drop_all() # move to seed.py
db.create_all()

graham = User(first_name="Graham", last_name="Trail") # move to seed.py
brit = User(first_name = "Brit", last_name="Juravic") # move to seed.py

db.session.add(graham) # move to seed.py
db.session.add(brit) # move to seed.py
db.session.commit() # move to seed.py

@app.route("/")
def user_list():
    "DOCSTRING"
    users = User.query.all()

    return render_template("list.html", users = users)

@app.route("/new-user")
def new_user_form():
    "DOCSTRING"

    return render_template("new_user_form.html")

@app.route("/user-submit", methods=["POST"])
def user_submit():

    first_name = request.form.get("first_name", "UNSET")
    last_name = request.form.get("last_name", "UNSET")
    image_url = request.form.get("image_url", "UNSET")

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")