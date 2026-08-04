from app import app
from extensions import db
from models import User

with app.app_context():

    user = User.query.filter_by(username="Nikhil").first()

    if user:

        user.role = "ADMIN"

        db.session.commit()

        print("User is now ADMIN.")

    else:

        print("User not found.")