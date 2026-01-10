from datetime import datetime, timedelta
from agenda import app, database, bcrypt, Usuario
from flask import url_for, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from agenda.models import HorariosDisponiveis

def _parse_time(hhmm: str):
    return datetime.strptime(hhmm, "%H:%M").time()


@app.route("/", methods=['GET', 'POST'])
def home():
 return render_template('homepage.html')

@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        email_get = request.form.get("email_login")
        senha_get = request.form.get("senha_login")
     
        usuario_existe = Usuario.query.filter_by(email=email_get).first()
        
        if usuario_existe:
            if bcrypt.check_password_hash(usuario_existe.senha_hash, senha_get):
               login_user(usuario_existe)
               if current_user.tipo == "Cliente":
                   return redirect(url_for("perfil_usuario"))
               else:
                   return redirect(url_for("perfil_profissional"))
            else: 
                flash("Senha incorreta. Tente Novamente", "danger")
                return redirect(url_for("login"))

        else:
            flash("Essa conta num existe", "danger")


    return redirect(url_for("home"))

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

@app.route('/marcar-horario', methods=['GET', 'POST'])
def marcar_horario():
    return render_template("marcar_horario.html")

@app.route('/perfil-usuario')
def perfil_usuario():
    return render_template("perfil_usuario.html")

@app.route('/perfil-profissional')
def perfil_profissional():
    return render_template("perfil_profissional.html")

@app.route('/sair', methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Você foi deslogado.", "primary")
    return redirect(url_for('home'))

@login_required
@app.route('/criar-slots', methods=['POST'])
def criar_slots():
    
    #pegar dados do form

    id_profissional = int(request.form['id_profissional'])
    data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()

    hora_inicio = _parse_time(request.form["hora_inicio"])
    hora_fim = _parse_time(request.form["hora_fim"])
    duracao = int(request.form["duracao_min"])

    #validacoes

    dt_inici = datetime.combine(data, hora_inicio)
    dt_fim = datetime.combine(data, hora_fim)

    if dt_fim <= dt_inici:
        flash("Hora final maior que hora inicial", "danger")
        return redirect(url_for("perfil_profissional"))
    
    if duracao <= 0:
        flash("Duração inválida", "danger")
        return redirect(url_for("perfil_profissional"))
    
    if id_profissional != current_user.id:
        flash("Ação não permitida", "danger")
        return redirect(url_for("perfil_profissional"))
    
    #gerando slots

    atual = dt_inici
    criados = 0

    while atual + timedelta(minutes=duracao) <= dt_fim:
        hora_slot = atual.time()

        ja_existe = HorariosDisponiveis.query.filter_by(
        id_profissional=id_profissional,
        data=data,
        hora=hora_slot
                        ).first()



        if not ja_existe:
            slot = HorariosDisponiveis(
                id_profissional=id_profissional,
                data=data,
                hora=hora_slot,
                ocupado=False
            )

        database.session.add(slot)
        criados +=1
        
    database.session.commit()
    flash("Horario criado.")
    return redirect(url_for("perfil_profissional"))
    
@app.route("/criar-slots", methods=["GET"])
def tela_criar_slots():
    return render_template("perfil_profissional.html")
