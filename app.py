import os
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "barbearia-celos-mvp-2026-chave-segura")

# Usuários iniciais com hash PBKDF2-HMAC-SHA256 (sem senhas em texto limpo)
USUARIOS = {
    "marcelo": {
        "nome": "Marcelo Silva",
        "senha_hash": generate_password_hash("celos2026", method="pbkdf2:sha256"),
    }
}

AGENDAMENTOS = [
    {"id": 1, "horario": "13:30", "cliente": "Rafael Souza", "whatsapp": "(41) 99999-0002", "servico": "Corte Masculino", "valor": 35.0, "pagamento": "PIX", "status": "CONCLUIDO"},
    {"id": 2, "horario": "14:00", "cliente": "Carlos Mendes", "whatsapp": "(41) 99999-0001", "servico": "Corte Masculino", "valor": 35.0, "pagamento": "PENDENTE", "status": "AGENDADO"},
]

HORARIOS_BASE = ["13:30", "14:00", "14:30", "15:00", "16:00", "16:30", "17:30"]

HTML_BASE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Barbearia Celos — Agendamento & Caixa</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #f4f6f9; }
    .app-container { max-width: 480px; margin: 0 auto; background: #fff; min-height: 100vh; box-shadow: 0 0 20px rgba(0,0,0,0.08); }
    .btn-touch { min-height: 48px; font-weight: 600; }
    .form-control, .form-select { min-height: 48px; border: 1.5px solid #495057; }
  </style>
</head>
<body>
<div class="app-container">
  <header class="bg-dark text-white p-3 d-flex justify-content-between align-items-center">
    <div>
      <div class="fw-bold fs-5">✂️ Barbearia Celos</div>
      <small class="text-light">Tatuquara • Curitiba - PR</small>
    </div>
    {% if session.get('usuario') %}
      <a href="{{ url_for('logout') }}" class="btn btn-outline-light btn-sm py-2 px-3">Sair</a>
    {% else %}
      <a href="{{ url_for('login') }}" class="btn btn-outline-light btn-sm py-2 px-3">🔒 Equipe</a>
    {% endif %}
  </header>

  <main class="p-3">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% for cat, msg in messages %}
        <div class="alert alert-{{ cat }} border border-dark fw-semibold" role="alert">{{ msg }}</div>
      {% endfor %}
    {% endwith %}
    {{ conteudo|safe }}
  </main>
</div>
</body>
</html>
"""

@app.route("/health")
def health():
    return {"status": "UP", "service": "barbearia-celos-mvp", "timestamp": datetime.utcnow().isoformat()}, 200

@app.route("/", methods=["GET", "POST"])
def index():
    ocupados = {a["horario"] for a in AGENDAMENTOS if a["status"] != "CANCELADO"}
    livres = [h for h in HORARIOS_BASE if h not in ocupados]

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        whatsapp = request.form.get("whatsapp", "").strip()
        horario = request.form.get("horario", "").strip()
        if not nome or not whatsapp or horario not in livres:
            flash("⚠ Horário indisponível ou dados incompletos. Escolha outro horário livre.", "warning")
            return redirect(url_for("index"))
        AGENDAMENTOS.append({
            "id": len(AGENDAMENTOS) + 1,
            "horario": horario,
            "cliente": nome,
            "whatsapp": whatsapp,
            "servico": "Corte Masculino",
            "valor": 35.0,
            "pagamento": "PENDENTE",
            "status": "AGENDADO",
        })
        flash(f"✓ Horário confirmado para {nome} às {horario} com Marcelo!", "success")
        return redirect(url_for("index"))

    opcoes_horarios = "".join([f'<option value="{h}">{h} — Livre</option>' for h in livres]) or '<option disabled>Sem horários livres hoje</option>'
    conteudo = f"""
    <h1 class="h5 fw-bold mb-3">Agende seu horário</h1>
    <form method="POST">
      <div class="mb-3">
        <label for="servico" class="form-label fw-bold">1. Serviço</label>
        <input id="servico" class="form-control" value="Corte Masculino — R$ 35,00 (30 min)" readonly>
      </div>
      <div class="mb-3">
        <label for="horario" class="form-label fw-bold">2. Horário Disponível</label>
        <select id="horario" name="horario" class="form-select" required>{opcoes_horarios}</select>
      </div>
      <div class="mb-3">
        <label for="nome" class="form-label fw-bold">3. Nome Completo *</label>
        <input id="nome" name="nome" type="text" class="form-control" placeholder="Ex: Carlos Mendes" required>
      </div>
      <div class="mb-3">
        <label for="whatsapp" class="form-label fw-bold">4. WhatsApp (com DDD) *</label>
        <input id="whatsapp" name="whatsapp" type="tel" class="form-control" placeholder="(41) 99999-0000" required>
      </div>
      <button type="submit" class="btn btn-primary w-100 btn-touch">✓ Confirmar Agendamento</button>
    </form>
    """
    return render_template_string(HTML_BASE, conteudo=conteudo)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("usuario", "").strip().lower()
        senha = request.form.get("senha", "")
        if user in USUARIOS and check_password_hash(USUARIOS[user]["senha_hash"], senha):
            session["usuario"] = user
            return redirect(url_for("painel"))
        flash("⚠ Credenciais inválidas.", "danger")
    conteudo = """
    <h1 class="h5 fw-bold mb-3">Acesso Restrito — Equipe</h1>
    <form method="POST">
      <div class="mb-3">
        <label for="usuario" class="form-label fw-bold">Usuário</label>
        <input id="usuario" name="usuario" class="form-control" value="marcelo" required>
      </div>
      <div class="mb-3">
        <label for="senha" class="form-label fw-bold">Senha</label>
        <input id="senha" name="senha" type="password" class="form-control" placeholder="••••••••" required>
      </div>
      <button type="submit" class="btn btn-dark w-100 btn-touch">Entrar no Painel</button>
      <a href="/" class="btn btn-outline-secondary w-100 btn-touch mt-2">← Voltar</a>
    </form>
    """
    return render_template_string(HTML_BASE, conteudo=conteudo)

@app.route("/painel")
def painel():
    if not session.get("usuario"):
        return redirect(url_for("login"))
    concluidos = [a for a in AGENDAMENTOS if a["status"] == "CONCLUIDO"]
    total = sum(a["valor"] for a in concluidos)
    comissao = total * 0.5
    cards = ""
    for a in sorted(AGENDAMENTOS, key=lambda x: x["horario"]):
        badge = '<span class="badge bg-success">✓ CONCLUÍDO</span>' if a["status"] == "CONCLUIDO" else '<span class="badge bg-warning text-dark border border-dark">⏳ AGENDADO</span>'
        acao = ""
        if a["status"] == "AGENDADO":
            acao = f"""
            <form method="POST" action="/concluir/{a['id']}" class="d-flex gap-2 mt-2">
              <select name="pagamento" class="form-select">
                <option value="PIX">PIX</option>
                <option value="DINHEIRO">DINHEIRO</option>
                <option value="CARTAO">CARTÃO</option>
              </select>
              <button class="btn btn-success btn-touch px-3">✓ Concluir</button>
            </form>"""
        cards += f"""
        <div class="card border-dark mb-2">
          <div class="card-body p-2">
            <div class="d-flex justify-content-between align-items-center">
              <strong>{a['horario']} — {a['cliente']}</strong>
              {badge}
            </div>
            <small class="text-muted">{a['servico']} • R$ {a['valor']:.2f} ({a['pagamento']})</small>
            {acao}
          </div>
        </div>"""
    conteudo = f"""
    <div class="card border-dark mb-3">
      <div class="card-header bg-dark text-white fw-bold">Resumo do Caixa Diário</div>
      <div class="card-body p-2">
        <div class="d-flex justify-content-between"><span>Total Recebido:</span><strong>R$ {total:.2f}</strong></div>
        <div class="d-flex justify-content-between"><span>Comissão Barbeiro (50%):</span><strong class="text-success">R$ {comissao:.2f}</strong></div>
      </div>
    </div>
    <h2 class="h6 fw-bold mb-2">Fila de Atendimentos</h2>
    {cards}
    """
    return render_template_string(HTML_BASE, conteudo=conteudo)

@app.route("/concluir/<int:ag_id>", methods=["POST"])
def concluir(ag_id):
    if not session.get("usuario"):
        return redirect(url_for("login"))
    pgto = request.form.get("pagamento", "PIX")
    for a in AGENDAMENTOS:
        if a["id"] == ag_id:
            a["status"] = "CONCLUIDO"
            a["pagamento"] = pgto
            flash(f"✓ Atendimento de {a['cliente']} concluído ({pgto})!", "success")
            break
    return redirect(url_for("painel"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
