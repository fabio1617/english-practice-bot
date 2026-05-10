# ============================================
# ARQUIVO: main.py (na raiz do projeto)
# ============================================

import sys
import os

# Detecta se está rodando como executável ou script
if getattr(sys, 'frozen', False):
    # Rodando como executável compilado
    BASE_DIR = sys._MEIPASS
else:
    # Rodando como script Python normal
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

def main():
    print("=" * 50)
    print("   ENGLISH PRACTICE BOT - FAETEC")
    print("=" * 50)
    print("\nEscolha o modo de execução:")
    print("1. Interface Gráfica (CustomTkinter)")
    print("2. Terminal")
    print("0. Sair")
    
    opcao = input("\nOpção: ")
    
    if opcao == "1":
        try:
            from frontend.english_bot_app import EnglishBotApp
            app = EnglishBotApp()
            app.rodar()
        except ImportError as e:
            print(f"Erro ao importar: {e}")
            print("Certifique-se de que o customtkinter está instalado: pip install customtkinter")
    
    elif opcao == "2":
        from backend.chat_bot import ChatBot
        bot = ChatBot()
        bot.iniciar()
    
    elif opcao == "0":
        print("Até mais!")
    
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()