# ============================================
# ARQUIVO: backend/chat_bot.py (VERSÃO CORRIGIDA)
# ============================================

import sys
import os

# Detecta caminho base (funciona no .exe e no script)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from backend.perguntas import CENARIOS

class ChatBot:
    def __init__(self):
        self.nome_aluno = ""
        self.pontuacao = 0
        self.cenarios = CENARIOS

    def mostrar_introducao(self):
        """Mostra introdução uma única vez no início"""
        print("=" * 50)
        print("   🎓 ENGLISH PRACTICE BOT - FAETEC")
        print("=" * 50)
        print()
        print("Olá! Este é um projeto de extensão desenvolvido por")
        print("Fábio Macedo, aluno de ADS - Análise e Desenvolvimento")
        print("de Sistemas pela instituição Veiga de Almeida.")
        print("Na FAETEC está cursando Inglês Básico.")
        print()
        print("Objetivo: Praticar diálogos em inglês de forma interativa.")
        print("=" * 50)
        print()

        self.nome_aluno = input("Digite seu nome: ")
        print(f"\nWelcome, {self.nome_aluno}! Let's practice! 🚀\n")

    def mostrar_menu(self):
        """Mostra opções disponíveis"""
        print("\n" + "=" * 50)
        print("CENÁRIOS DISPONÍVEIS:")
        print("=" * 50)

        cenario_lista = list(self.cenarios.keys())
        for i, cenario in enumerate(cenario_lista, 1):
            print(f"{i}. {cenario}")
        print("0. Sair")
        print("-" * 50)

        escolha = input("Escolha uma opção: ")

        if escolha == '0':
            print(f"\nObrigado por praticar, {self.nome_aluno}!")
            return False

        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(cenario_lista):
                cenario_escolhido = cenario_lista[indice]
                self.executar_cenario(cenario_escolhido)
                return True
            else:
                print("❌ Opção inválida! Tente novamente.")
                return True
        except ValueError:
            print("❌ Digite um número válido!")
            return True

    def executar_cenario(self, cenario):
        """Executa um cenário de conversação completo"""
        passos = self.cenarios[cenario]
        acertos = 0
        total = len(passos)

        print(f"\n{'=' * 50}")
        print(f"   🎯 INICIANDO: {cenario.upper()}")
        print(f"{'=' * 50}")
        print("💡 Responda em INGLÊS! Use frases completas quando possível.\n")
        print("📌 ATENÇÃO: Use letra MAIÚSCULA no início da frase e ponto final!\n")

        for i, passo in enumerate(passos, 1):
            print(f"\n--- Pergunta {i}/{total} ---")
            print(f"🤖 Bot: {passo['pergunta']}")

            tentativas = 0
            acertou = False

            while tentativas < 3 and not acertou:
                resposta = input("\nSua resposta: ").strip()  # Remove .lower() para manter maiúscula
                
                # Remove espaços extras mas mantém maiúscula e ponto
                resposta = resposta.strip()

                if not resposta:
                    print("⚠️  Você não digitou nada! Tente novamente.")
                    tentativas += 1
                    continue

                # Verifica se a resposta está exatamente correta
                if resposta in passo['respostas']:
                    self.dar_feedback(True)
                    acertos += 1
                    self.pontuacao += 10
                    acertou = True
                else:
                    tentativas_restantes = 2 - tentativas
                    # Passa a resposta do usuário e a resposta correta para o feedback
                    self.dar_feedback(False, passo['respostas'], tentativas_restantes, resposta, passo['respostas'][0])
                    tentativas += 1

            if not acertou:
                print(f"💡 Resposta sugerida: {passo['respostas'][0]}")
                print("   Não desanime! Lembre-se: letra MAIÚSCULA no início e ponto final! 💪")

            print("-" * 40)

        # Mostra resultado do cenário
        percentual = (acertos / total) * 100
        print(f"\n{'=' * 50}")
        print(f"   📊 RESULTADO DO CENÁRIO: {cenario}")
        print(f"{'=' * 50}")
        print(f"   ✅ Acertos: {acertos}/{total}")
        print(f"   📈 Aproveitamento: {percentual:.1f}%")
        print(f"   🎯 Pontos ganhos: {acertos * 10}")
        print(f"{'=' * 50}")

        # Feedback motivacional
        if percentual == 100:
            print("🎉 PARABÉNS! Você acertou tudo! Excelente! 🎉")
        elif percentual >= 70:
            print("👍 Muito bom! Continue praticando! 👍")
        elif percentual >= 50:
            print("📚 Bom trabalho! Com mais prática você melhora ainda mais! 📚")
        else:
            print("💪 Continue praticando! A prática leva à perfeição! 💪")

        input("\nPressione ENTER para voltar ao menu...")

    def verificar_resposta(self, resposta_usuario, respostas_corretas):
        """Verifica se a resposta está exatamente correta"""
        return resposta_usuario in respostas_corretas

    def dar_feedback(self, acertou, dicas=None, tentativas_restantes=0, resposta_usuario=None, resposta_correta=None):
        """Dá feedback ao aluno com dicas específicas sobre gramática"""
        if acertou:
            print("\n✅ MUITO BEM! Resposta correta! +10 pontos")
        else:
            print(f"\n❌ Resposta incorreta! ({tentativas_restantes} tentativas restantes)")
        
            # Verifica problemas específicos com maiúscula/pontuação
            if resposta_usuario and resposta_correta:
                # Caso 1: Só diferença de maiúscula/minúscula
                if resposta_usuario.lower() == resposta_correta.lower():
                    if resposta_usuario[0].islower():
                        print("💡 Dica: A frase deve começar com letra MAIÚSCULA!")
                    elif not resposta_usuario.endswith(('.', '!', '?')):
                        print("💡 Dica: Não esqueça a PONTUAÇÃO no final da frase (. ! ?)!")
                    else:
                        print(f"💡 Dica: A forma correta é: {resposta_correta}")
            
                # Caso 2: Problemas com pontuação específica
                elif resposta_usuario.lower().rstrip('.!?') == resposta_correta.lower().rstrip('.!?'):
                    if resposta_usuario.endswith('.'):
                        print("💡 Dica: Esta frase parece ser interrogativa. Use '?' no final!")
                    elif resposta_usuario.endswith('!'):
                        print("💡 Dica: Esta frase parece ser afirmativa. Use '.' no final!")
                    elif not resposta_usuario.endswith(('.', '!', '?')):
                        print("💡 Dica: Adicione a pontuação correta no final da frase! (. ! ?)")
            
                # Caso 3: Falta pontuação
                elif not resposta_usuario.endswith(('.', '!', '?')):
                    pontuacao_esperada = '.'
                    if '?' in resposta_correta:
                        pontuacao_esperada = '?'
                    elif '!' in resposta_correta:
                        pontuacao_esperada = '!'
                    print(f"💡 Dica: Não esqueça a pontuação! Use '{pontuacao_esperada}' no final da frase!")
            
                # Caso 4: Primeira letra minúscula
                elif resposta_usuario.lower().capitalize().rstrip('.!?') == resposta_correta.lower().rstrip('.!?'):
                    print("💡 Dica: Lembre-se de começar com letra MAIÚSCULA!")
            
                else:
                    print(f"💡 Dica: A forma correta é: {resposta_correta}")
            else:
                if dicas:
                    dicas_mostrar = dicas[:3]
                    print(f"💡 Dica: Respostas possíveis: {', '.join(dicas_mostrar)}")

    def iniciar(self):
        """Método principal que controla o fluxo"""
        self.mostrar_introducao()

        continuar = True
        while continuar:
            continuar = self.mostrar_menu()

        self.mostrar_resumo_final()

    def mostrar_resumo_final(self):
        """Mostra resumo do desempenho"""
        print(f"\n{'=' * 50}")
        print("   📊 RESUMO FINAL")
        print(f"{'=' * 50}")
        print(f"👨‍🎓 Aluno: {self.nome_aluno}")
        print(f"⭐ Pontuação total: {self.pontuacao} pontos")

        # Mensagem motivacional baseada na pontuação
        if self.pontuacao >= 100:
            print("🏆 EXCELENTE! Você é um ótimo aluno! 🏆")
        elif self.pontuacao >= 50:
            print("👍 MUITO BOM! Continue praticando! 👍")
        elif self.pontuacao > 0:
            print("💪 BOM TRABALHO! Com dedicação você vai longe! 💪")
        else:
            print("🌟 Não desista! Na próxima tente responder mais perguntas! 🌟")

        print(f"{'=' * 50}")
        print("Obrigado por participar da pesquisa!")
        print("Projeto de extensão - Fábio Macedo")
        print(f"{'=' * 50}")