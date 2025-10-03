import functools
import requests
from flask import Flask, request, session, render_template, redirect, url_for, g, flash, Response

# --- Configuração da Aplicação ---
app = Flask(__name__)
# Chave secreta para gerenciar sessões de usuário de forma segura.
# Em um ambiente de produção, isso deve ser uma string longa e aleatória.
app.config["SECRET_KEY"] = "dev"

# --- "Banco de Dados" de Usuários Simulado ---
# Para esta prova de conceito, usaremos um usuário fixo.
# Em um sistema real, isso viria de um banco de dados.
USERS = {"aluno@exemplo.com": "senha123"}

# --- SIMULAÇÃO DE BANCO DE DADOS DE ARQUIVOS ---
# Associa um ID interno a um link real do Google Drive.
# NOTA: O link do Google Drive deve ser o de download direto.
# Para obtê-lo, use o formato: https://drive.google.com/uc?export=download&id=SEU_FILE_ID
GOOGLE_DRIVE_FILES = {
    "VIDEO_AULA_1": "https://drive.google.com/uc?export=download&id=ID_DO_SEU_VIDEO_AQUI",
    "PDF_AULA_1": "https://drive.google.com/uc?export=download&id=ID_DO_SEU_PDF_AQUI",
}

# --- Middleware e Hooks de Requisição ---

@app.before_request
def load_logged_in_user():
    """Carrega o usuário logado da sessão antes de cada requisição."""
    user_email = session.get("user_email")
    g.user = user_email if user_email else None

def login_required(view):
    """
    Decorador que redireciona usuários não logados para a página de login.
    Garante que certas rotas só sejam acessíveis por usuários autenticados.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

# --- Definição de Rotas (Views) ---

@app.route("/login", methods=("GET", "POST"))
def login():
    """Processa o formulário de login e gerencia a sessão do usuário."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if email not in USERS or USERS[email] != password:
            error = "Credenciais inválidas. Tente novamente."

        if error is None:
            # Limpa a sessão anterior e armazena o novo usuário.
            session.clear()
            session["user_email"] = email
            # Redireciona para a página solicitada ou para o painel.
            next_url = request.args.get('next')
            return redirect(next_url or url_for("dashboard"))

        flash(error)

    # Se o usuário já estiver logado, redireciona para o painel.
    if g.user:
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Limpa a sessão do usuário, efetivamente fazendo o logout."""
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    """Painel principal do aluno, acessível apenas após o login."""
    # Simula uma lista de aulas disponíveis.
    aulas = [
        {"id": 1, "titulo": "Aula 1: Introdução ao Inglês", "concluida": True},
        {"id": 2, "titulo": "Aula 2: Verbos Essenciais", "concluida": False},
    ]
    return render_template("dashboard.html", aulas=aulas)

@app.route("/aula/<int:id>")
@login_required
def aula(id):
    """Exibe uma aula específica com seu vídeo e material."""
    # Para esta PoC, usamos um ID fixo. Em um sistema real, isso viria do banco.
    aula_info = {
        "id": id,
        "titulo": f"Aula {id}: Conteúdo Detalhado",
        "video_id": "VIDEO_AULA_1",
        "material_id": "PDF_AULA_1"
    }
    return render_template("aula.html", aula=aula_info)

@app.route("/conteudo_protegido/<path:file_id>")
@login_required
def conteudo_protegido(file_id):
    """
    Endpoint do Proxy de Conteúdo. Verifica o login e atua como um intermediário
    seguro para buscar conteúdo do Google Drive sem expor o link original.
    """
    real_url = GOOGLE_DRIVE_FILES.get(file_id)
    if not real_url:
        return "Conteúdo não encontrado.", 404

    # Usamos stream=True para não carregar o arquivo inteiro na memória do servidor.
    # Isso é vital para arquivos grandes como vídeos.
    try:
        req = requests.get(real_url, stream=True)
        req.raise_for_status()  # Lança um erro para respostas HTTP ruins (4xx ou 5xx)

        # Transmite o conteúdo do Google Drive para o cliente.
        # O Flask lida com o streaming do gerador `req.iter_content`.
        # Passamos os cabeçalhos originais, como Content-Type e Content-Length.
        return Response(req.iter_content(chunk_size=1024),
                        content_type=req.headers.get('Content-Type'))
    except requests.exceptions.RequestException as e:
        # Em caso de falha ao buscar o conteúdo (ex: link quebrado, sem permissão)
        app.logger.error(f"Falha ao buscar conteúdo do Google Drive: {e}")
        return "Erro ao acessar o conteúdo remoto.", 502 # Bad Gateway

if __name__ == "__main__":
    # Executa a aplicação em modo de desenvolvimento.
    # O host 0.0.0.0 torna a aplicação acessível na rede local.
    app.run(debug=True, host="0.0.0.0", port=5001)