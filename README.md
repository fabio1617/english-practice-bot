# 🎓 English Practice Bot

Bot de prática de inglês interativo desenvolvido como **Atividade de Extensão** do curso de Análise e Desenvolvimento de Sistemas (ADS) da Universidade Veiga de Almeida (UVA), em parceria com a **FAETEC – Vila Isabel**.

---

## 🌍 ODS 4 – Educação de Qualidade

> *"Assegurar a educação inclusiva e equitativa e de qualidade, e promover oportunidades de aprendizagem ao longo da vida para todas e todos."*
> — Agenda 2030, ONU

Este projeto contribui diretamente para o **Objetivo de Desenvolvimento Sustentável 4** ao oferecer uma ferramenta educacional digital **gratuita e acessível** para alunos que buscam aprender inglês sem acesso a recursos pagos.

---

## 📌 Sobre o Projeto

O **English Practice Bot** é uma aplicação desktop que permite aos alunos praticarem traduções e estruturas gramaticais do inglês de forma interativa, com feedback imediato, sistema de pontuação e barra de progresso.

**Comunidade atendida:** Alunos do curso de Inglês Básico da FAETEC – Escola Técnica Estadual de Vila Isabel, Rio de Janeiro.

**Problema resolvido:** A ausência de ferramentas digitais gratuitas e adaptadas ao nível básico que permitam a prática do inglês fora da sala de aula.

---

## 🖥️ Funcionalidades

- ✅ 5 aulas com mais de 130 exercícios de tradução
- ✅ Feedback imediato com dicas gramaticais e de pontuação
- ✅ Até 3 tentativas por pergunta
- ✅ Sistema de pontuação acumulada
- ✅ Barra de progresso por aula
- ✅ Links para vídeos explicativos de cada aula
- ✅ Ranking de pontuações (acesso restrito ao professor)
- ✅ Interface gráfica moderna com tema escuro
- ✅ Distribuição como arquivo `.exe` (sem necessidade de instalar Python)

---

## 📚 Conteúdo das Aulas

| Aula | Conteúdo |
|------|----------|
| Aula 1 | Simple Present – I, you, we, they |
| Aula 2 | Simple Present – she, he, it |
| Aula 3 | Presente Simples – Interrogativos |
| Aula 4 | Presente Simples – Pronomes objeto |
| Aula 5 | Passado Simples |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9**
- **CustomTkinter** – Interface gráfica
- **Flask** – API REST para ranking
- **SQLite** – Banco de dados local
- **PyInstaller** – Geração do executável `.exe`
- **python-dotenv** – Gerenciamento de variáveis de ambiente

---

## 📁 Estrutura do Projeto

```
english-practice-bot/
├── backend/
│   ├── app.py          # API REST (Flask)
│   ├── chat_bot.py     # Lógica do chatbot
│   ├── database.py     # Conexão com SQLite
│   ├── models.py       # Modelo de dados (Ranking)
│   └── perguntas.py    # Banco de perguntas e respostas
├── frontend/
│   └── english_bot_app.py  # Interface gráfica (CustomTkinter)
├── main.py             # Ponto de entrada
├── main.spec           # Configuração do PyInstaller
├── requirements.txt    # Dependências do projeto
├── .env                # Variáveis de ambiente (não versionado)
└── .gitignore
```

---

## ⚙️ Como Executar

### Opção 1 — Executável (recomendado)

Baixe o arquivo `EnglishPracticeBot.exe` na pasta `dist/` e execute diretamente.
Não é necessário instalar Python ou qualquer dependência.

### Opção 2 — Código fonte

**1. Clone o repositório**
```bash
git clone https://github.com/fabio1617/english-practice-bot.git
cd english-practice-bot
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Crie o arquivo `.env`** na raiz do projeto
```
SENHA_PROFESSOR=sua_senha_aqui
```

**4. Execute a aplicação**
```bash
python main.py
```

### Gerar o executável

```bash
pyinstaller main.spec
```
O arquivo `.exe` será gerado em `dist/EnglishPracticeBot.exe`.

---

## 🔒 Segurança

A senha de acesso ao ranking do professor é armazenada em variável de ambiente (`.env`) e **não é versionada no repositório**. O arquivo `.env` está listado no `.gitignore`.

---

## 👤 Autor

**Fábio Macedo**
Aluno de ADS – Universidade Veiga de Almeida (UVA)
Curso de Inglês Básico – FAETEC Vila Isabel

Agradecimento especial ao **Prof. Waniston** pelo apoio e orientação neste projeto.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como Atividade de Extensão Universitária.
