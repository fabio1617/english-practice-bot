import sqlite3
import os
import sys

# Detecta caminho base
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Coloca o banco na MESMA PASTA do executável (ou do script)
# Se for .exe, usa a pasta onde o .exe está. Se for script, usa a pasta do script.
if getattr(sys, 'frozen', False):
    DB_FOLDER = os.path.dirname(sys.executable)  # Pasta do .exe
else:
    DB_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Raiz do projeto

DB_NAME = os.path.join(DB_FOLDER, "ranking.db")

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pontuacao INTEGER NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()