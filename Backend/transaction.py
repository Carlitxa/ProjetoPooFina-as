class Transaction:
    def __init__(self, id, descricao, valor, data, tipo, categoria):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.tipo = tipo      # "receita" ou "despesa"
        self.categoria = categoria
