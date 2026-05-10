# ============================================
# ARQUIVO: frontend/english_bot_app.py
# VERSÃO COM SIDEBAR AJUSTADA PARA TEXTOS LONGOS
# ============================================

import customtkinter as ctk
import sys
import os
import threading
from datetime import datetime
import requests
import webbrowser

# Detecta caminho base (funciona tanto compilado quanto script)
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

# Agora importa normalmente
from backend.chat_bot import ChatBot


# ============ CONSTANTES DE ESTILO ============
class Theme:
    """Cores e estilos centralizados para fácil manutenção"""
    BG_PRIMARY = "#1a1a2e"        # Fundo principal (azul escuro)
    BG_SECONDARY = "#16213e"      # Fundo secundário
    BG_CARD = "#0f3460"           # Fundo dos cards
    ACCENT = "#e94560"            # Cor de destaque (vermelho/rosa)
    SUCCESS = "#00d9ff"           # Verde água para acertos
    ERROR = "#ff6b6b"             # Vermelho para erros
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a0a0a0"
    BOT_BUBBLE = "#2d3561"        # Balão do bot
    USER_BUBBLE = "#1e5631"       # Balão do usuário
    FONT_FAMILY = "Segoe UI"      # Fonte moderna (ou "Helvetica", "Roboto")


class EnglishBotApp:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ctk.CTk()
        self.janela.title("🎓 English Practice \nBot - FAETEC")
        self.janela.geometry("1100x700")  # Aumentei a largura total
        self.janela.minsize(900, 600)
        
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Configurar grid principal: [sidebar | chat_area]
        self.janela.grid_columnconfigure(0, weight=0)  # Sidebar fixa
        self.janela.grid_columnconfigure(1, weight=1)  # Chat expande
        self.janela.grid_rowconfigure(0, weight=1)
        
        # Estado do chat
        self.chatbot = None
        self.cenario_atual = None
        self.pergunta_atual_index = 0
        self.total_perguntas = 0
        self.passos = []
        self.tentativas = 0
        self.acertos = 0
        self.mensagens_widgets = []  # Referências para limpar se necessário
        
        # Cria os widgets da tela inicial
        self.criar_tela_inicial()
        
    def criar_tela_inicial(self):
        """Tela de boas-vindas com design moderno centralizado"""
        
        # Frame principal centralizado
        self.frame_inicial = ctk.CTkFrame(
            self.janela, 
            fg_color=Theme.BG_PRIMARY,
            corner_radius=20
        )
        self.frame_inicial.place(relx=0.5, rely=0.5, anchor="center")
        
        # Container interno para padding
        container = ctk.CTkFrame(self.frame_inicial, fg_color="transparent")
        container.pack(padx=60, pady=60)
        
        # Ícone/Emoji grande
        ctk.CTkLabel(
            container,
            text="🎓",
            font=(Theme.FONT_FAMILY, 64)
        ).pack(pady=(0, 10))
        
        # Título
        ctk.CTkLabel(
            container, 
            text="English Practice Bot",
            font=(Theme.FONT_FAMILY, 32, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(pady=10)
        
        # Subtítulo
        ctk.CTkLabel(
            container,
            text="Projeto de Extensão - Fábio Macedo 2026\nCurso: Análise e Desenvolvimento de Sistemas (ADS)\nInstituição Universidade Veiga de Almeida - UVA.\n FAETEC - Vila Isabel",
            font=(Theme.FONT_FAMILY, 14),
            text_color=Theme.TEXT_SECONDARY,
            justify="center"
        ).pack(pady=(0, 30))
        
        # Separador visual
        separador = ctk.CTkFrame(container, height=2, fg_color=Theme.ACCENT)
        separador.pack(fill="x", pady=20)
        
        # Campo de nome estilizado
        ctk.CTkLabel(
            container, 
            text="Qual é o seu nome?",
            font=(Theme.FONT_FAMILY, 16, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(pady=(10, 5))
        
        self.nome_entry = ctk.CTkEntry(
            container, 
            width=350, 
            height=50, 
            font=(Theme.FONT_FAMILY, 16),
            placeholder_text="Digite seu nome aqui...",
            corner_radius=10,
            border_width=2,
            border_color=Theme.BG_CARD
        )
        self.nome_entry.pack(pady=10)
        self.nome_entry.bind("<Return>", lambda e: self.iniciar_chat())
        
        # Botão iniciar com hover effect
        self.botao_iniciar = ctk.CTkButton(
            container,
            text="Começar a Praticar! 🚀",
            command=self.iniciar_chat,
            width=350,
            height=50,
            corner_radius=10,
            font=(Theme.FONT_FAMILY, 16, "bold"),
            fg_color=Theme.ACCENT,
            hover_color="#ff2e4d",
            text_color="white"
        )
        self.botao_iniciar.pack(pady=20)
        
        # Dica no rodapé
        ctk.CTkLabel(
            container,
            text="💡 Dica: Use letra maiúscula no início e pontuação no final!",
            font=(Theme.FONT_FAMILY, 12),
            text_color=Theme.TEXT_SECONDARY
        ).pack(pady=(10, 0))
        
    def criar_tela_chat(self):
        """Interface principal dividida em sidebar + área de chat"""
        
        # Remove tela inicial
        self.frame_inicial.destroy()
        
        # ========== SIDEBAR (Esquerda) - AJUSTADA ==========
        self.sidebar = ctk.CTkFrame(
            self.janela,
            width=320,  # AUMENTADO: de 280 para 320
            fg_color=Theme.BG_SECONDARY,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)  # Mantém largura fixa
        
        # Cabeçalho da sidebar
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(20, 10))  # REDUZIDO padding horizontal
        
        ctk.CTkLabel(
            header,
            text="📚 Aulas",
            font=(Theme.FONT_FAMILY, 18, "bold"),  # REDUZIDO: de 20 para 18
            text_color=Theme.TEXT_PRIMARY
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Escolha um cenário",
            font=(Theme.FONT_FAMILY, 11),  # REDUZIDO: de 12 para 11
            text_color=Theme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(3, 0))
        
        # Separador
        ctk.CTkFrame(self.sidebar, height=2, fg_color=Theme.BG_CARD).pack(fill="x", padx=15, pady=5)
        
        # Container scrollável para lista de cenários
        self.cenarios_container = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            scrollbar_button_color=Theme.BG_CARD
        )
        self.cenarios_container.pack(fill="both", expand=True, padx=10, pady=5)  # REDUZIDO padding
        
        # Info do usuário no rodapé da sidebar
        self.user_info_frame = ctk.CTkFrame(self.sidebar, fg_color=Theme.BG_CARD, corner_radius=10)
        self.user_info_frame.pack(fill="x", padx=15, pady=15)
        
        self.user_name_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"👤 {self.chatbot.nome_aluno}",
            font=(Theme.FONT_FAMILY, 13, "bold"),  # REDUZIDO: de 14 para 13
            text_color=Theme.TEXT_PRIMARY
        )
        self.user_name_label.pack(pady=8)  # REDUZIDO: de 10 para 8
        
        self.score_sidebar_label = ctk.CTkLabel(
            self.user_info_frame,
            text="⭐ Pontuação: 0",
            font=(Theme.FONT_FAMILY, 11),  # REDUZIDO: de 12 para 11
            text_color=Theme.SUCCESS
        )
        self.score_sidebar_label.pack(pady=(0, 8))
        
        # ========== ÁREA PRINCIPAL DE CHAT (Direita) ==========
        self.chat_area = ctk.CTkFrame(self.janela, fg_color=Theme.BG_PRIMARY)
        self.chat_area.grid(row=0, column=1, sticky="nsew")
        self.chat_area.grid_rowconfigure(1, weight=1)  # Mensagens expandem
        self.chat_area.grid_columnconfigure(0, weight=1)
        
        # --- Header do chat ---
        self.chat_header = ctk.CTkFrame(self.chat_area, fg_color=Theme.BG_SECONDARY, height=60)
        self.chat_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.chat_header.grid_propagate(False)
        
        self.header_titulo = ctk.CTkLabel(
            self.chat_header,
            text="🤖 English Practice Bot",
            font=(Theme.FONT_FAMILY, 18, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        self.header_titulo.place(relx=0.5, rely=0.5, anchor="center")
        
        # Indicador de status
        self.status_label = ctk.CTkLabel(
            self.chat_header,
            text="● Online",
            font=(Theme.FONT_FAMILY, 12),
            text_color=Theme.SUCCESS
        )
        self.status_label.place(relx=0.95, rely=0.5, anchor="e")
        
        # --- Área de mensagens (Scrollable) ---
        self.mensagens_frame = ctk.CTkScrollableFrame(
            self.chat_area,
            fg_color=Theme.BG_PRIMARY,
            scrollbar_button_color=Theme.BG_CARD
        )
        self.mensagens_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # --- Área de pergunta atual (destaque) ---
        self.pergunta_frame = ctk.CTkFrame(
            self.chat_area,
            fg_color=Theme.BG_CARD,
            corner_radius=15
        )
        self.pergunta_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.pergunta_label = ctk.CTkLabel(
            self.pergunta_frame,
            text="🤖 Bot: Escolha uma aula na sidebar para começar!",
            font=(Theme.FONT_FAMILY, 14, "bold"),
            wraplength=600,
            text_color=Theme.TEXT_PRIMARY
        )
        self.pergunta_label.pack(pady=15, padx=20)
        
        # --- Área de entrada ---
        input_frame = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        input_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.resposta_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite sua resposta em inglês aqui...",
            height=50,
            font=(Theme.FONT_FAMILY, 14),
            corner_radius=10,
            border_width=2,
            border_color=Theme.BG_CARD
        )
        self.resposta_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.resposta_entry.bind("<Return>", lambda e: self.enviar_resposta())
        
        self.botao_enviar = ctk.CTkButton(
            input_frame,
            text="➤",
            command=self.enviar_resposta,
            width=50,
            height=50,
            corner_radius=10,
            font=(Theme.FONT_FAMILY, 20),
            fg_color=Theme.ACCENT,
            hover_color="#ff2e4d"
        )
        self.botao_enviar.grid(row=0, column=1)
        
        # --- Barra de progresso ---
        self.progress_frame = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=8,
            corner_radius=4,
            fg_color=Theme.BG_CARD,
            progress_color=Theme.SUCCESS
        )
        self.progress_bar.pack(fill="x", side="left", expand=True, padx=(0, 15))
        self.progress_bar.set(0)
        
        self.progress_text = ctk.CTkLabel(
            self.progress_frame,
            text="0/0",
            font=(Theme.FONT_FAMILY, 12),
            text_color=Theme.TEXT_SECONDARY,
            width=50
        )
        self.progress_text.pack(side="right")
        
        # --- Botão voltar ---
        self.botao_menu = ctk.CTkButton(
            self.chat_area,
            text="◀ Voltar ao Menu de Aulas",
            command=self.voltar_menu,
            width=200,
            height=35,
            corner_radius=8,
            font=(Theme.FONT_FAMILY, 12),
            fg_color="transparent",
            border_color=Theme.TEXT_SECONDARY,
            border_width=1,
            text_color=Theme.TEXT_SECONDARY,
            hover_color=Theme.BG_CARD
        )
        self.botao_menu.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="w")
        
        # Popula a sidebar com cenários
        self.popular_sidebar_cenarios()
        
        # Mensagem de boas-vindas no chat
        self.adicionar_mensagem_bot(
            f"Olá, {self.chatbot.nome_aluno}! 👋\n\n"
            f"Bem-vindo ao English Practice Bot!\nVamos praticar inglês juntos 🚀\n\n"
            f"⚠️ REGRAS: ⚠️\n"
            f"• Comece a frase com letra maiúscula.\n"
            f"• Termine com ponto final (.)\n"
            f"• Use ! ou ? quando necessário\n\n"
            f"Escolha uma aula na sidebar à esquerda para começar!"
        )
        
    def popular_sidebar_cenarios(self):
        """Cria cards clicáveis para cada cenário na sidebar - AJUSTADO PARA TEXTOS LONGOS"""
        cenario_lista = list(self.chatbot.cenarios.keys())
        
        for i, cenario in enumerate(cenario_lista, 1):
            # Frame principal do card com altura dinâmica
            card = ctk.CTkFrame(
                self.cenarios_container,
                fg_color=Theme.BG_CARD,
                corner_radius=8,  # REDUZIDO: de 10 para 8
                cursor="hand2"
            )
            card.pack(fill="x", pady=3, padx=2)  # REDUZIDO: pady de 5 para 3
            card.bind("<Button-1>", lambda e, c=cenario: self.abrir_cenario(c))
            
            # Layout horizontal: número | texto | seta
            # Usamos um frame interno para melhor controle
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=8, pady=6)  # REDUZIDO: padding interno
            
            # Número da aula - MAIS COMPACTO
            numero = ctk.CTkLabel(
                inner,
                text=f"{i}",
                font=(Theme.FONT_FAMILY, 14, "bold"),  # REDUZIDO: de 20 para 14
                text_color=Theme.ACCENT,
                width=25  # REDUZIDO: de 40 para 25
            )
            numero.pack(side="left", padx=(0, 6))  # REDUZIDO: espaçamento
            
            # Container para o nome (permite wrap se necessário, mas preferimos fonte menor)
            texto_frame = ctk.CTkFrame(inner, fg_color="transparent")
            texto_frame.pack(side="left", fill="both", expand=True)
            
            # Nome do cenário - FONTE MENOR E WRAP
            nome = ctk.CTkLabel(
                texto_frame,
                text=cenario,
                font=(Theme.FONT_FAMILY, 11, "bold"),  # REDUZIDO: de 13 para 11
                text_color=Theme.TEXT_PRIMARY,
                anchor="w",
                justify="left",
                wraplength=210  # NOVO: quebra linha se necessário (ajustado para nova largura)
            )
            nome.pack(fill="x", anchor="w")
            
            # Ícone de seta - MAIS DISCRETO
            seta = ctk.CTkLabel(
                inner,
                text="›",  # MUDADO: de "▶" para "›" (mais compacto)
                font=(Theme.FONT_FAMILY, 16, "bold"),  # REDUZIDO
                text_color=Theme.TEXT_SECONDARY,
                width=15  # REDUZIDO: de 30 para 15
            )
            seta.pack(side="right", padx=(4, 0))
            
            # Hover effect
            def on_enter(event, f=card):
                f.configure(fg_color="#1a4a7a")
            def on_leave(event, f=card):
                f.configure(fg_color=Theme.BG_CARD)
                
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            # Tornar todos os widgets filhos clicáveis também
            for widget in [numero, nome, seta, inner, texto_frame]:
                widget.bind("<Button-1>", lambda e, c=cenario: self.abrir_cenario(c))
                
    def adicionar_mensagem_bot(self, mensagem):
        """Adiciona balão de mensagem do bot (lado esquerdo)"""
        container = ctk.CTkFrame(self.mensagens_frame, fg_color="transparent")
        container.pack(fill="x", pady=5, anchor="w")
        
        balao = ctk.CTkFrame(
            container,
            fg_color=Theme.BOT_BUBBLE,
            corner_radius=15
        )
        balao.pack(side="left", padx=(0, 50))
        
        header = ctk.CTkFrame(balao, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            header,
            text="🤖 Bot",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            text_color="#6b8cff"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%H:%M"),
            font=(Theme.FONT_FAMILY, 10),
            text_color=Theme.TEXT_SECONDARY
        ).pack(side="right")
        
        texto = ctk.CTkLabel(
            balao,
            text=mensagem,
            font=(Theme.FONT_FAMILY, 13),
            text_color=Theme.TEXT_PRIMARY,
            wraplength=500,
            justify="left"
        )
        texto.pack(padx=15, pady=(0, 15))
        
        self.mensagens_frame._parent_canvas.yview_moveto(1.0)
        
    def adicionar_mensagem_usuario(self, mensagem):
        """Adiciona balão de mensagem do usuário (lado direito)"""
        container = ctk.CTkFrame(self.mensagens_frame, fg_color="transparent")
        container.pack(fill="x", pady=5, anchor="e")
        
        balao = ctk.CTkFrame(
            container,
            fg_color=Theme.USER_BUBBLE,
            corner_radius=15
        )
        balao.pack(side="right", padx=(50, 0))
        
        header = ctk.CTkFrame(balao, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            header,
            text=datetime.now().strftime("%H:%M"),
            font=(Theme.FONT_FAMILY, 10),
            text_color="#7dd87d"
        ).pack(side="left")
        
        ctk.CTkLabel(
            header,
            text="Você 👤",
            font=(Theme.FONT_FAMILY, 11, "bold"),
            text_color="#7dd87d"
        ).pack(side="right")
        
        texto = ctk.CTkLabel(
            balao,
            text=mensagem,
            font=(Theme.FONT_FAMILY, 13),
            text_color=Theme.TEXT_PRIMARY,
            wraplength=500,
            justify="right"
        )
        texto.pack(padx=15, pady=(0, 15))
        
        self.mensagens_frame._parent_canvas.yview_moveto(1.0)
        
    def adicionar_mensagem_sistema(self, mensagem, tipo="info"):
        """Adiciona mensagem de sistema centralizada (feedback, erros, etc)"""
        container = ctk.CTkFrame(self.mensagens_frame, fg_color="transparent")
        container.pack(fill="x", pady=10)
        
        cores = {
            "info": ("#3d3d5c", Theme.TEXT_SECONDARY),
            "sucesso": (Theme.SUCCESS, Theme.BG_PRIMARY),
            "erro": (Theme.ERROR, Theme.BG_PRIMARY),
            "aviso": ("#f0a500", Theme.BG_PRIMARY)
        }
        
        bg_color, text_color = cores.get(tipo, cores["info"])
        
        label = ctk.CTkLabel(
            container,
            text=mensagem,
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=text_color,
            fg_color=bg_color,
            corner_radius=20,
            padx=20,
            pady=8
        )
        label.pack()
        
        self.mensagens_frame._parent_canvas.yview_moveto(1.0)
        
    def iniciar_chat(self):
        """Inicia o chat com o nome do aluno"""
        nome = self.nome_entry.get().strip()
        
        if not nome:
            self.nome_entry.configure(border_color=Theme.ERROR)
            self.janela.after(2000, lambda: self.nome_entry.configure(border_color=Theme.BG_CARD))
            return
        
        self.chatbot = ChatBot()
        self.chatbot.nome_aluno = nome
        self.cenario_atual = None
        
        self.criar_tela_chat()

    def abrir_cenario(self, cenario):
        """Abre vídeo ou inicia aula"""

        dados = self.chatbot.cenarios[cenario]

        # Se for vídeo
        if isinstance(dados, dict) and dados.get("tipo") == "video":

            link = dados.get("link")

            self.adicionar_mensagem_sistema(
                "🎥 Abrindo vídeo aula no navegador...",
                tipo="info"
            )

            webbrowser.open(link)

            return

        # Se for aula normal
        self.iniciar_cenario(cenario)

    def iniciar_cenario(self, cenario):
        """Inicia um cenário de perguntas"""
        self.cenario_atual = cenario
        self.passos = self.chatbot.cenarios[cenario]
        self.total_perguntas = len(self.passos)
        self.pergunta_atual_index = 0
        self.tentativas = 0
        self.acertos = 0
        
        self.atualizar_progresso()
        
        self.adicionar_mensagem_sistema(f"🎯 Iniciando: {cenario}", tipo="info")
        
        self.mostrar_proxima_pergunta()
        
    def mostrar_proxima_pergunta(self):
        """Mostra a próxima pergunta do cenário"""
        if self.pergunta_atual_index >= self.total_perguntas:
            self.finalizar_cenario()
            return
            
        passo = self.passos[self.pergunta_atual_index]
        pergunta = passo['pergunta']
        self.respostas_corretas = passo['respostas']
        
        self.adicionar_mensagem_bot(pergunta)
        self.pergunta_label.configure(text=f"🤖 {pergunta}")
        
        self.tentativas = 0
        
        self.resposta_entry.delete(0, "end")
        self.resposta_entry.focus()
        
    def enviar_resposta(self):
        """Processa a resposta do aluno"""
        resposta = self.resposta_entry.get().strip()
        
        if not resposta:
            return
        
        self.adicionar_mensagem_usuario(resposta)
        self.resposta_entry.delete(0, "end")
        
        if self.cenario_atual is None:
            self.adicionar_mensagem_bot("Por favor, escolha uma aula na sidebar à esquerda.")
        else:
            self.processar_resposta_cenario(resposta)
            
    def processar_resposta_cenario(self, resposta):
        """Processa a resposta do aluno para uma pergunta do cenário"""
        
        passo = self.passos[self.pergunta_atual_index]
        respostas_corretas = passo['respostas']
        resposta_correta = respostas_corretas[0]
        
        if resposta in respostas_corretas:
            self.chatbot.pontuacao += 10
            self.acertos += 1
            self.atualizar_pontuacao()
            self.atualizar_progresso()
            
            self.adicionar_mensagem_sistema("✅ MUITO BEM! Resposta correta! +10 pontos", tipo="sucesso")
            
            self.pergunta_atual_index += 1
            self.mostrar_proxima_pergunta()
            
        else:
            self.tentativas += 1
            tentativas_restantes = 3 - self.tentativas
            
            if tentativas_restantes > 0:
                dica = self.gerar_dica(resposta, resposta_correta)
                self.adicionar_mensagem_sistema(
                    f"❌ Resposta incorreta! ({tentativas_restantes} tentativas restantes)", 
                    tipo="erro"
                )
                if dica:
                    self.adicionar_mensagem_bot(f"💡 {dica}")
            else:
                self.adicionar_mensagem_sistema("❌ Acabaram as tentativas!", tipo="erro")
                self.adicionar_mensagem_bot(f"💡 Resposta correta: **{resposta_correta}**")
                
                self.pergunta_atual_index += 1
                self.mostrar_proxima_pergunta()
                
    def gerar_dica(self, resposta_usuario, resposta_correta):
        """Gera uma dica específica baseada no erro do aluno"""
        
        if resposta_usuario.lower() == resposta_correta.lower():
            if resposta_usuario[0].islower():
                return "A frase deve começar com letra MAIÚSCULA!"
            elif not resposta_usuario.endswith(('.', '!', '?')):
                return "Não esqueça a PONTUAÇÃO no final da frase (. ! ?)!"
            else:
                return f"A forma correta é: {resposta_correta}"
        
        elif resposta_usuario.lower().rstrip('.!?') == resposta_correta.lower().rstrip('.!?'):
            if resposta_usuario.endswith('.'):
                return "Esta frase parece ser interrogativa. Use '?' no final!"
            elif resposta_usuario.endswith('!'):
                return "Esta frase parece ser afirmativa. Use '.' no final!"
            else:
                return f"Adicione a pontuação correta! Use a que termina em: {resposta_correta[-1]}"
        
        elif not resposta_usuario.endswith(('.', '!', '?')):
            pontuacao_esperada = '.'
            if '?' in resposta_correta:
                pontuacao_esperada = '?'
            elif '!' in resposta_correta:
                pontuacao_esperada = '!'
            return f"Não esqueça a pontuação! Use '{pontuacao_esperada}' no final da frase!"
        
        else:
            return f"A forma correta é: {resposta_correta}"
        
    def atualizar_pontuacao(self):
        """Atualiza labels de pontuação em todos os lugares"""
        texto = f"⭐ Pontuação: {self.chatbot.pontuacao}"
        self.score_sidebar_label.configure(text=texto)
        
    def atualizar_progresso(self):
        """Atualiza barra de progresso"""
        if self.total_perguntas > 0:
            progresso = self.pergunta_atual_index / self.total_perguntas
            self.progress_bar.set(progresso)
            self.progress_text.configure(text=f"{self.pergunta_atual_index}/{self.total_perguntas}")
        else:
            self.progress_bar.set(0)
            self.progress_text.configure(text="0/0")
        
    def finalizar_cenario(self):
        """Finaliza o cenário e mostra o resultado"""
        percentual = (self.acertos / self.total_perguntas) * 100 if self.total_perguntas > 0 else 0
        
        self.adicionar_mensagem_sistema("📊 RESULTADO FINAL", tipo="info")
        
        resultado_texto = (
            f"✅ **Acertos:** {self.acertos}/{self.total_perguntas}\n"
            f"📈 **Aproveitamento:** {percentual:.1f}%\n"
            f"🎯 **Pontos ganhos:** {self.acertos * 10}"
        )
        self.adicionar_mensagem_bot(resultado_texto)
        
        if percentual == 100:
            self.adicionar_mensagem_sistema("🎉 PARABÉNS! Você acertou tudo! Excelente!", tipo="sucesso")
        elif percentual >= 70:
            self.adicionar_mensagem_sistema("👍 Muito bom! Continue praticando!", tipo="sucesso")
        elif percentual >= 50:
            self.adicionar_mensagem_sistema("📚 Bom trabalho! Com mais prática você melhora ainda mais!", tipo="aviso")
        else:
            self.adicionar_mensagem_sistema("💪 Continue praticando! A prática leva à perfeição!", tipo="aviso")
        
        self.adicionar_mensagem_bot("Escolha outra aula na sidebar para continuar praticando!")
        self.pergunta_label.configure(text="🤖 Aula concluída! Escolha outra no menu.")
        self.cenario_atual = None
        
        threading.Thread(target=self.salvar_pontuacao_api).start()
        
    def voltar_menu(self):
        """Volta ao menu de cenários"""
        self.cenario_atual = None
        self.pergunta_label.configure(text="🤖 Escolha uma aula na sidebar para começar!")
        self.adicionar_mensagem_sistema("◀ Voltando ao menu de aulas", tipo="info")
        self.progress_bar.set(0)
        self.progress_text.configure(text="0/0")
        
    def salvar_pontuacao_api(self):
        try:
            url = "http://127.0.0.1:5000/salvar"
            data = {
                "nome": self.chatbot.nome_aluno,
                "pontuacao": self.chatbot.pontuacao
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Pontuação salva com sucesso")
            else:
                print("Erro ao salvar")
        except Exception as e:
            print("Erro:", e)
        
    def rodar(self):
        """Inicia a aplicação"""
        self.janela.mainloop()


# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    app = EnglishBotApp()
    app.rodar()