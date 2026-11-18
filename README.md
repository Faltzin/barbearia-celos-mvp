# ✂️ Barbearia Celos — MVP de Agendamento e Controle de Caixa

Sistema web responsivo (**mobile-first**) desenvolvido como Projeto de Extensão / Experiência Prática do curso de **Análise e Desenvolvimento de Sistemas (ADS)** da **Cruzeiro do Sul Virtual**, em parceria com a **Barbearia Celos** (Tatuquara, Curitiba – PR).

## 🎯 Objetivo e Alinhamento ao ODS 8
Eliminar conflitos de horário, ociosidade de cadeiras e falhas no fechamento financeiro manual (caderno/WhatsApp), contribuindo diretamente para a **Meta 8.3 do ODS 8** (*Trabalho Decente e Crescimento Econômico*).

## 🛠️ Stack Tecnológica e Arquitetura
* **Arquitetura:** Monolítica em 3 Camadas (Apresentação, Regras de Negócio e Persistência)
* **Linguagem / Runtime:** Python 3.12
* **Backend / Templates:** Flask 3.0 + Jinja2
* **Frontend / Acessibilidade:** HTML5 + Bootstrap 5.3 (WCAG, áreas de toque ≥ 44×44 px, contraste ≥ 4,5:1)
* **ORM / Banco de Dados:** SQLAlchemy 2.0 + PostgreSQL 16
* **Segurança:** Hashing PBKDF2-HMAC-SHA256 (`werkzeug.security`) e controles contra OWASP Top 10

## 📁 Estrutura Planejada do Projeto
```text
barbearia-celos-mvp/
├── app.py                 # Rotas Flask, autenticação e regras de negócio
├── models.py              # Entidades SQLAlchemy (clientes, barbeiros, agendamentos, lancamentos_caixa)
├── templates/             # Telas HTML responsivas (Jinja2 + Bootstrap 5.3)
├── requirements.txt       # Dependências fixadas do ambiente Python
├── .env.example           # Modelo de variáveis de ambiente (DATABASE_URL, SECRET_KEY)
└── README.md              # Documentação técnica do MVP
