from agenda import database
from flask_login import UserMixin
from datetime import datetime
from flask import request




class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, unique=True,nullable=False)
    email = database.Column(database.String, nullable=False)
    senha_hash = database.Column(database.String, nullable=False)
    tipo = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False)

    
    def create(nome, email, senha_hash, tipo_user, n_telefone):
                usuario = Usuario(nome=nome,
                           email=email, 
                           senha_hash=senha_hash, 
                           tipo=tipo_user, 
                           telefone=n_telefone)
                return usuario

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
