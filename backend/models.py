import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from backend.database import conectar

class Ranking:

    @staticmethod
    def adicionar(nome, pontuacao):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO ranking (nome, pontuacao) VALUES (?, ?)",
            (nome, pontuacao)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def listar():
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT nome, pontuacao, data 
        FROM ranking 
        ORDER BY pontuacao DESC
        """)

        dados = cursor.fetchall()
        conn.close()

        return [
            {"nome": n, "pontuacao": p, "data": d}
            for (n, p, d) in dados
        ]