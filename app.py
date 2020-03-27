"""Blogly application."""

from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from seed import setup_db

app = Flask(__name__)

app.config["SECRET_KEY"] = "Shhhhh"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

setup_db()

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
    image_url = request.form.get("image_url") or None

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

    return render_template("user_detail.html",
                            user=current_user)

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
    image_url = request.form.get("image_url") or None

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


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    "Renders page that displays form to add a new post"

    current_user = User.query.get_or_404(user_id)

    return render_template('add_post_form.html', user=current_user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_submit(user_id):
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_details(post_id):
    "Shows the post."

    post = Post.query.get_or_404(post_id)

    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    "Deletes a specific post from the database."

    post = Post.query.get_or_404(post_id)

    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>/edit")
def post_edit(post_id):
    "Shows the post editing form."

    post = Post.query.get_or_404(post_id)

    return render_template("edit_post_form.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def post_edit_submit(post_id):
    "Submits the changes to the post."

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/tags")
def list_tags():
    "Lists all tags."

    tags = Tag.query.all()

    return render_template("list_tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """Lists all posts with specific tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_detail.html", tag=tag)