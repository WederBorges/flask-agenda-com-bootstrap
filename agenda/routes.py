from agenda import app
from flask import url_for, render_template



@app.route("/")
def home():
    return render_template('base.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/marcar-horario')
def marcar_horario():
    return render_template("marcar_horario.html")

