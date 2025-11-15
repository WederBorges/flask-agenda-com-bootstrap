from agenda import database, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, unique=True,nullable=False)
    email = database.Column(database.String, nullable=False)
    senha_hash = database.Column(database.String, nullable=False)
    tipo = database.Column(database.String, nullable=False)

class HorariosDisponiveis(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data = database.Column(database.Date, nullable=False)
    hora = database.Column(database.Time, nullable=False)

class RegistrosAgendamento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    profissional_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    cliente_id = database.Column(database.Integer,database.ForeignKey('usuario.id'), nullable=False)
    horario_id = database.Column(database.Integer,database.ForeignKey('horarios_disponiveis.id'), nullable=False)
    status = database.Column(database.String, nullable=False)
