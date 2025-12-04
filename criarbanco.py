from agenda import app, database
from agenda import models

with app.app_context():
    database.drop_all()
    database.create_all()