from models import db, User, Post, Tag, PostTag

def setup_db():
    "Function for setting up database each time we run app.py"
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()
    Tag.query.delete()
    PostTag.query.delete()

    # Add users
    graham = User(first_name="Graham", last_name="Trail")
    brit = User(first_name="Brit", last_name="Juravic")

    # Add posts
    post_1 = Post(title="First Post",
                  content="This is our first post",
                  user_id=1)
    post_2 = Post(title="Second Post",
                  content="This is our second post",
                  user_id=2)

    # Add tags
    tag_1 = Tag(name="tag1")
    tag_2 = Tag(name="tag2")

    # Add posts_tags
    post_tag_1 = PostTag(post_id=1, tag_id=1)
    post_tag_2 = PostTag(post_id=2, tag_id=2)
    post_tag_3 = PostTag(post_id=1, tag_id=2)
    post_tag_4 = PostTag(post_id=2, tag_id=1)

    # Add new objects to session, so they'll persist
    db.session.add(graham)
    db.session.add(brit)
    db.session.commit()

    db.session.add(post_1)
    db.session.add(post_2)
    db.session.commit()

    db.session.add(tag_1)
    db.session.add(tag_2)
    db.session.commit()

    db.session.add(post_tag_1)
    db.session.add(post_tag_2)
    db.session.add(post_tag_3)
    db.session.add(post_tag_4)

    # Commit--otherwise, this never gets saved!
    db.session.commit()
