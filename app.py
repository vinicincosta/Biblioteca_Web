import token

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.routing import BuildError
from functools import wraps
import routes

import datetime
from werkzeug.security import generate_password_hash

from routes import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            flash('Você deve entrar com uma conta para acessar o sistema', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    # 1️⃣ Se o usuário clicou no botão "Entrar"
    if request.method == 'POST':
        try:
            # 2️⃣ Pegando dados do formulário
            email = request.form.get('email')
            password = request.form.get('senha')

            print(email, password)

            # 3️⃣ Enviando para a API / função de login
            user = routes.post_login(email, password)

            # 4️⃣ Se o login deu certo (tem token)
            if 'access_token' in user:

                session['user_id'] = routes.get_usuarios(user['access_token'])
                session['token'] = user['access_token']
                session['username'] = user['nome']
                session['papel'] = user['papel']

                # 5️⃣ Redireciona conforme o papel
                if session['papel'] == 'admin':
                    flash('Bem-vindo administrador', 'success')
                    return redirect(url_for('usuarios'))

                elif session['papel'] == 'usuario':
                    flash('Bem-vindo cozinheiro', 'success')
                    return redirect(url_for('usuarios'))

                else:
                    flash('Você não tem acesso a esse sistema', 'error')
                    return redirect(url_for('login'))

            # 6️⃣ Se o login falhar
            else:
                if user.get('erro') == '401':
                    flash('Email ou senha inválidos', 'error')
                else:
                    flash('Erro ao tentar logar', 'error')

                return render_template('login.html')

        # 7️⃣ Erro inesperado
        except Exception as e:
            print("Erro no login:", e)
            flash("Erro inesperado", "error")
            return render_template('login.html')

    # 8️⃣ Quando acessa a página pela primeira vez
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logout realizado com sucesso', 'success')
    return redirect(url_for('login'))



API_TOKEN = "SEU_TOKEN_REAL_DA_API"

@app.route('/usuarios')
@login_required
def usuarios():
    usuarios = get_usuarios(API_TOKEN)

    if 'erro' in usuarios:
        return f"Erro na API: {usuarios}", 500

    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/livros')
@login_required
def livros():
     livros = get_livros(API_TOKEN)

     if 'erro' in livros:
         return f"Erro na API: {livros}", 500

     return render_template('livros.html', livros=livros)

@app.route('/livros_disponiveis')
@login_required
def livros_disponiveis():
    livros_disponiveis = get_livros_disponiveis()

    if 'erro' in livros_disponiveis:
        flash("Nenhum livro disponivel")

    return render_template('livros_disponiveis.html', livros_disponiveis=livros_disponiveis)


@app.route('/livros_emprestados')
@login_required
def livros_emprestados():

    livros_emprestados = get_livros_emprestados()

    if 'erro' in livros_emprestados:
        flash("Nenhum livro emprestado")

    return render_template('livros_emprestados.html', livros_emprestados=livros_emprestados)

@app.route('/historico_de_emprestimos_por_usuario/<int:id_usuario>')
@login_required
def historico_de_emprestimos_por_usuario(id_usuario):

    usuarios_emp = get_historico_de_emprestimos_por_usuario(id_usuario)

    if 'error' in usuarios_emp:
        flash("Este usuário não realizou empréstimos")
        return redirect(url_for('usuarios'))



    return render_template(
        'historico_user.html',
        usuarios_emp=usuarios_emp
    )


@app.route('/emprestimos')
@login_required
def emprestimos():
    emprestimos = get_emprestimos(API_TOKEN)

    if 'erro' in emprestimos:
        return f"Erro na API: {emprestimos}", 500

    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/livros/cadastrar_livro/', methods=['GET', 'POST'])
@login_required
def cadastrar_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        ISBN = request.form.get('ISBN')
        resumo = request.form.get('resumo')
        leitura = request.form.get('leitura')
        token = API_TOKEN

        if not all([titulo, autor, ISBN, resumo, leitura]):
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('cadastrar_livro'))

        resultado = post_livro(token,titulo, autor, ISBN, resumo, leitura)

        if resultado == 200:
            flash('Livro cadastrado com sucesso!', 'success')
            return redirect(url_for('livros'))

        else:
            flash('erro em cadastrar livro .', 'error')
            return redirect(url_for('cadastrar_livro'))

    return render_template('cadastrar_livro.html')




@app.route('/editar_usuario/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id_usuario):
    try:
        if request.method == 'GET':
            usuario = get_usuario_por_id(id_usuario)

            if not usuario:
                flash('Usuário não encontrado', 'danger')
                return redirect(url_for('usuarios'))

            return render_template(
                'editar_usuario.html',
                usuario=usuario
            )

        elif request.method == 'POST':
            nome = request.form.get('nome')
            endereco = request.form.get('endereco')
            email = request.form.get('email')
            status_user = request.form.get('status_user')
            papel = request.form.get('papel')
            cpf = request.form.get('cpf')


            resultado = put_editar_usuario(
                id_usuario,
                nome,
                papel,
                status_user,
                email,
                endereco,
                cpf

            )

            # Talvez mudar depois o http 302 para 201, 302 significa redirecionamento temporário
            if resultado == 302:
                flash('Usuário editado com sucesso!', 'success')
            else:
                flash('Erro ao editar usuário.', 'danger')

            return redirect(url_for('usuarios'))

    except Exception as e:
        flash(f"Erro ao atualizar: {str(e)}", "danger")
        return redirect(url_for('usuarios'))


@app.route('/editar_livro/<int:id_livro>', methods=['GET', 'POST'])
@login_required
def editar_livro(id_livro):
    try:
        if request.method == 'GET':
            livro = get_livro_por_id(id_livro)

            if not livro:
                flash("livro não encontrado", "danger")
                return redirect(url_for('livros'))

            return render_template(
                'editar_livro.html', livro=livro
            )

        elif request.method == 'POST':
            titulo = request.form.get('titulo')
            autor = request.form.get('autor')
            ISBN = request.form.get('ISBN')
            resumo = request.form.get('resumo')
            leitura = request.form.get('leitura')

            resultado = put_editar_livro(
                id_livro,
                titulo,
                autor,
                ISBN,
                resumo,
                leitura,
            )

            if resultado == 200:
                flash('Livro editado com sucesso!', 'success')

            else:
                flash("Erro ao editar livro.", "danger")
            return redirect(url_for('livros'))

    except Exception as e:
        flash(f"Erro ao atualizar: {str(e)}", "danger")
        return redirect(url_for('livros'))


@app.route('/deletar_livro/<int:id_livro>', methods=['POST'])
@login_required
def deletar_livro(id_livro):
    livros_delete = delete_livro(id_livro)

    if not livros_delete or 'erro' in livros_delete:
        flash('Erro ao deletar livro', 'danger')
        return redirect(url_for('livros'))

    flash('Livro deletado com sucesso!', 'success')
    return redirect(url_for('livros'))


# Livros que mais foram emprestados
@app.route("/dados_grafico_livros_emp")
def dados_grafico_livros_emp():
    if 'token' not in session:
        return jsonify({"erro": "Sem login"}), 401

    dados = routes.get_livros_mais_emp()

    return jsonify(dados)


@app.route("/dados_grafico_livros_emp_html")
def dados_grafico_livros_emp_html():
    return render_template("dashboard.html")



# Usuários que mais realizaram empréstimos
@app.route("/dados_usuarios_que_mais_realizaram_emp")
def dados_usuarios_que_mais_realizaram_emp():
    if 'token' not in session:
        return jsonify({"erro": "Sem login"}), 401

    dados = routes.get_usuarios_que_mais_realizaram_emp()
    print(dados)

    return jsonify(dados)



if __name__ == '__main__':
    app.run(debug=True)