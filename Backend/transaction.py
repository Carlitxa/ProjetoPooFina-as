class Transaction:
    def __init__(self, id, descricao, valor, data, tipo, categoria):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.tipo = tipo
        self.categoria = categoria

    def validar_valor(self):
        pass
