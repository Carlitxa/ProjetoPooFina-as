from flask import Flask, render_template, request, redirect, url_for
from Backend.finance_manager import FinanceManager
from Backend.user import User

"""
Aplicação web para gestão de finanças pessoais.
Permite gerir utilizadores, transações, categorias e relatórios.
Desenvolvida no âmbito da unidade curricular de Programação Orientada a Objetos.
"""


app = Flask(
    __name__,
    template_folder="Web/Templates",
    static_folder="Web/Static"
)

app.secret_key = "segredo_super_importante"

finance = FinanceManager()


# ---------- PÁGINA INICIAL ----------
@app.route("/")
def index():
    return render_template("index.html")


# ---------- REGISTO ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]

        novo = User(
            id=len(finance.users) + 1,
            nome=nome,
            email=email,
            password=password,
            perfil="user"
        )

        finance.adicionar_utilizador(novo)
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = finance.autenticar(email, password)
        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Login inválido"

    return render_template("login.html")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------- CATEGORIAS ----------
@app.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        nome = request.form["nome"]
        finance.adicionar_categoria(nome)
        return redirect(url_for("categories"))

    return render_template("categories.html", categorias=finance.categories)


# ---------- ADICIONAR TRANSAÇÃO ----------
@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = request.form["valor"]
        categoria = request.form["categoria"]
        tipo = request.form["tipo"]   # "receita" ou "despesa"

        finance.adicionar_transacao(descricao, valor, categoria, tipo)
        return redirect(url_for("list_transactions"))

    # GET: mostrar formulário
    return render_template("add_transaction.html", categorias=finance.categories)


# ---------- LISTAR TRANSAÇÕES ----------
@app.route("/list_transactions")
def list_transactions():
    transacoes = finance.listar_transacoes()
    return render_template("list_transactions.html", transacoes=transacoes)


# ---------- EDITAR TRANSAÇÃO ----------
@app.route("/edit_transaction/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    transacao = finance.obter_transacao(transaction_id)
    if transacao is None:
        return redirect(url_for("list_transactions"))

    if request.method == "POST":
        descricao = request.form["descricao"]
        valor = request.form["valor"]
        categoria = request.form["categoria"]
        tipo = request.form["tipo"]

        finance.editar_transacao(transaction_id, descricao, valor, categoria, tipo)
        return redirect(url_for("list_transactions"))

    # GET: mostrar formulário com dados preenchidos
    return render_template(
        "edit_transaction.html",
        transacao=transacao,
        categorias=finance.categories
    )


# ---------- ELIMINAR TRANSAÇÃO ----------
@app.route("/delete_transaction/<int:transaction_id>")
def delete_transaction(transaction_id):
    finance.eliminar_transacao(transaction_id)
    return redirect(url_for("list_transactions"))


# ---------- RELATÓRIOS ----------
@app.route("/reports")
def reports():
    total_r = finance.total_receitas()
    total_d = finance.total_despesas()
    saldo = finance.saldo_atual()

    despesas_cat = finance.despesas_por_categoria()
    labels = list(despesas_cat.keys())
    values = list(despesas_cat.values())

    return render_template(
        "reports.html",
        total_r=total_r,
        total_d=total_d,
        saldo=saldo,
        labels=labels,
        values=values
    )



if __name__ == "__main__":
    app.run(debug=True)
