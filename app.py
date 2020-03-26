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

@app.route("/")
def home():
    "Redirects visitor to users list."

    return redirect("/users")

@app.route("/users")
def user_list():
    "Shows a list of all users."
    users = User.query.all()

    return render_template("list.html", users=users)

@app.route("/users/new")
def new_user_form():
    "Shows a form to add a new user."

    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def user_submit():
    "Processes new user form and adds user to the database."

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if image_url == "":
        new_user = User(first_name=first_name,
                        last_name=last_name)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    "Shows details for specific user."

    current_user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=current_user)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    "Shows form to edit details for specific user."

    current_user = User.query.get_or_404(user_id)

    return render_template("user_edit.html", user=current_user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_submit(user_id):
    "Processes form for edits to a user and submits them to the database."

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    "Deletes a specific user from the database."

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")