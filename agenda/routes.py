from agenda import app, database, bcrypt, Usuario
from flask import url_for, render_template, request, redirect, url_for, flash



@app.route("/", methods=['GET', 'POST'])
def home():
 return render_template('homepage.html')

@app.route("/login", methods=["POST", "GET"])
def login():


    return render_template("login.html")

@app.route("/registre", methods=['GET', 'POST'])
def registre():
        
    if request.method =="POST":

        senha_cript = bcrypt.generate_password_hash(request.form.get("senha_register"))
        usuario = Usuario.create(
                           nome=request.form.get("nome_completo"),
                           email=request.form.get("email_register"), 
                           senha_hash=senha_cript, 
                           tipo=request.form.get("tipo_usuario"), 
                           telefone=request.form.get("num_tel"))
        
        email=request.form.get("email_register")
        if Usuario.query.filter_by(email=email).first():
            flash("Esse usuário já existe, mano. Tente outro e-mail", "danger")
            return redirect(url_for('registre'))
        else:
            database.session.add(usuario)
            database.session.commit()
            flash("Usuário criado com sucesso", "info")              
            return render_template("homepage.html")
    return render_template("homepage.html")

@app.route('/marcar-horario')
def marcar_horario():
    return render_template("marcar_horario.html")

@app.route('/perfil-usuario')
def perfil_usuario():
    return render_template("perfil_usuario.html")

@app.route('/perfil_profissional')
def perfil_profissional():
    return render_template("perfil_profissional.html")

