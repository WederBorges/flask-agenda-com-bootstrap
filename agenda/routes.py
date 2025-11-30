from agenda import app
from flask import url_for, render_template



@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registre")
def registre_se():
    return render_template("registre.html")

@app.route('/marcar-horario')
def marcar_horario():
    return render_template("marcar_horario.html")

@app.route('/perfil-usuario')
def perfil_usuario():
    return render_template("perfil_usuario.html")

@app.route('/perfil_profissional')
def perfil_profissional():
    return render_template("perfil_profissional.html")

