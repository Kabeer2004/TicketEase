import os
from app import app, db
from models import User, Ticket

# Set up an application context
with app.app_context():
    # Check if the site.db file exists in the instance folder
    db_path = os.path.join(app.instance_path, 'site.db')
    if os.path.exists(db_path):
        # Delete the existing site.db file
        os.remove(db_path)
        print("Existing database was deleted.")
    else:
        print("No existing database is present.")

    # Create all database tables
    db.create_all()
    print("New database is being created.")
