from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
graham = User(first_name="Graham", last_name="Trail") 
brit = User(first_name = "Brit", last_name="Juravic") 

# Add new objects to session, so they'll persist
db.session.add(graham)
db.session.add(brit)

# Commit--otherwise, this never gets saved!
db.session.commit()