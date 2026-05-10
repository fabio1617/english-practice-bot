import sys
import os

# Detecta caminho base (funciona no .exe e no script)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from flask import Flask, jsonify, request
from backend.models import Ranking
from backend.perguntas import CENARIOS
from backend.database import criar_tabela

SENHA_PROFESSOR = os.getenv("SENHA_PROFESSOR", "Faetec26042026")

app = Flask(__name__)

@app.route("/")
def home():
    return "API funcionando!"


@app.route("/salvar", methods=["POST"])
def salvar():
    data = request.json

    nome = data.get("nome")
    pontuacao = data.get("pontuacao")

    # validação
    if not nome or pontuacao is None:
        return jsonify({"erro": "Dados inválidos"}), 400

    try:
        pontuacao = int(pontuacao)
    except:
        return jsonify({"erro": "Pontuação inválida"}), 400

    Ranking.adicionar(nome, pontuacao)

    return jsonify({"mensagem": "Salvo com sucesso"})


@app.route("/ranking", methods=["GET"])
def ranking():
    senha = request.args.get("senha")

    if senha != SENHA_PROFESSOR:
        return jsonify({"erro": "Acesso negado"}), 403

    return jsonify(Ranking.listar())


@app.route("/cenarios", methods=["GET"])
def cenarios():
    return jsonify(list(CENARIOS.keys()))


if __name__ == "__main__":
    criar_tabela()  # ← cria o banco automaticamente
    app.run(debug=True)