from agenda import database
from flask_login import UserMixin
from datetime import datetime
from flask import request




class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer,   primary_key=True)
    nome = database.Column(database.String,  nullable=False)
    email = database.Column(database.String, unique=True, nullable=False)
    senha_hash = database.Column(database.String, nullable=False)
    tipo = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False)

    @staticmethod
    def create(nome, email, senha_hash, tipo, telefone):
                usuario = Usuario(nome=nome,
                           email=email, 
                           senha_hash=senha_hash, 
                           tipo=tipo, 
                           telefone=telefone)
                return usuario

class HorariosDisponiveis(database.Model):

    __tablename__ = "horarios_disponiveis" #define o nome da tabela no bd

    id = database.Column(database.Integer, primary_key=True)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    data = database.Column(database.Date, nullable=False)
    hora = database.Column(database.Time, nullable=False)

    ocupado = database.Column(database.Boolean, nullable=False, default=False)

    __table_args__ = (
        database.UniqueConstraint('id_profissional', 'data', 'hora', name='uq_prof_data_hora'),
    )


class RegistrosAgendamento(database.Model):

    __tablename__ = "registros_agendamento"

    id = database.Column(database.Integer, primary_key=True)
    id_profissional = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    cliente_id = database.Column(database.Integer,database.ForeignKey('usuario.id'), nullable=False)
    horario_id = database.Column(database.Integer,database.ForeignKey('horarios_disponiveis.id'), nullable=False, unique=True)
    status = database.Column(database.String, nullable=False, default="PENDENTE")

    slot = database.relationship("HorarioDisponiveis", backref="agendamentos")
    cliente = database.relationship("Usuario", foreign_keys=[cliente_id])
    profissional = database.relationship("Usuario", foreign_keys=[id_profissional])