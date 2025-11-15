from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bd_agendamento.db"
app.config["SECRET_KEY"] = "175b71a2a7685241681e95c54d34432d7559cb0107b27c75ab65d4034032c35c" 

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from agenda import routes