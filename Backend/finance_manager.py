from .category import Category
from .transaction import Transaction
from .user import User
from .file_storage import FileStorage
from datetime import date

# Classe que gere transações, categorias, users e relatórios
class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = []
        self.users = []

        # gestor de ficheiro
        self.storage = FileStorage()

        # tentar carregar dados do ficheiro (se existir)
        self.storage.carregar_dados(self)

        if not self.categories:
            self.categories = [
                Category("Alimentação"),
                Category("Transportes"),
                Category("Lazer"),
                Category("Saúde"),
                Category("Outros"),
            ]

    # ---------- UTILIZADORES ----------
    def adicionar_utilizador(self, user: User):
        self.users.append(user)
        self.storage.guardar_dados(self)

    def autenticar(self, email: str, password: str):
        for u in self.users:
            if u.email == email and u.password == password:
                return u
        return None

    # ---------- CATEGORIAS ----------
    def adicionar_categoria(self, nome: str):
        """Adiciona uma nova categoria, se ainda não existir."""
        nome = nome.strip()
        if not nome:
            return

        for c in self.categories:
            if c.nome.lower() == nome.lower():
                return  # já existe

        self.categories.append(Category(nome))
        self.storage.guardar_dados(self)

    # ---------- TRANSAÇÕES ----------
    def adicionar_transacao(self, descricao, valor, categoria_nome, tipo):
        """Cria e adiciona uma nova transação."""
        valor = float(valor)

        # garantir valor positivo
        if valor < 0:
            valor = abs(valor)

        # procurar categoria pelo nome
        categoria = None
        for c in self.categories:
            if c.nome == categoria_nome:
                categoria = c
                break

        # se não existir, criar nova categoria
        if categoria is None:
            categoria = Category(categoria_nome)
            self.categories.append(categoria)

        nova = Transaction(
            id=len(self.transactions) + 1,
            descricao=descricao,
            valor=valor,
            data=date.today().isoformat(),
            tipo=tipo,
            categoria=categoria,
        )

        self.transactions.append(nova)
        self.storage.guardar_dados(self)

    def listar_transacoes(self):
        return self.transactions

    def obter_transacao(self, trans_id: int):
        """Devolve a transação com o id indicado ou None se não existir."""
        for t in self.transactions:
            if t.id == trans_id:
                return t
        return None

    def editar_transacao(self, trans_id, descricao, valor, categoria_nome, tipo):
        """Altera os dados de uma transação existente."""
        transacao = self.obter_transacao(trans_id)
        if transacao is None:
            return False

        valor = float(valor)
        if valor < 0:
            valor = abs(valor)

        # procurar categoria
        categoria = None
        for c in self.categories:
            if c.nome == categoria_nome:
                categoria = c
                break

        if categoria is None:
            categoria = Category(categoria_nome)
            self.categories.append(categoria)

        transacao.descricao = descricao
        transacao.valor = valor
        transacao.tipo = tipo
        transacao.categoria = categoria

        self.storage.guardar_dados(self)
        return True

    def eliminar_transacao(self, trans_id):
        """Remove uma transação pelo id."""
        self.transactions = [t for t in self.transactions if t.id != trans_id]
        self.storage.guardar_dados(self)

    # ---------- RELATÓRIOS ----------
    def total_receitas(self):
        return sum(t.valor for t in self.transactions if t.tipo == "receita")

    def total_despesas(self):
        return sum(t.valor for t in self.transactions if t.tipo == "despesa")

    def saldo_atual(self):
        return self.total_receitas() - self.total_despesas()

    def despesas_por_categoria(self):
        """Devolve um dicionário {nome_categoria: total_despesas}."""
        totais = {}
        for t in self.transactions:
            if t.tipo != "despesa":
                continue
            nome = t.categoria.nome if t.categoria else "Sem categoria"
            totais[nome] = totais.get(nome, 0) + t.valor
        return totais
