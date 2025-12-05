import json
import os

from .user import User
from .transaction import Transaction
from .category import Category


class FileStorage:
    def __init__(self, filename="dados.json"):
        self.filename = filename

    def guardar_dados(self, finance_manager):
        """Guarda utilizadores, categorias e transações num ficheiro JSON."""
        data = {
            "users": [
                {
                    "id": u.id,
                    "nome": u.nome,
                    "email": u.email,
                    "password": u.password,
                    "perfil": u.perfil,
                }
                for u in finance_manager.users
            ],
            "categories": [
                {
                    "nome": c.nome
                }
                for c in finance_manager.categories
            ],
            "transactions": [
                {
                    "id": t.id,
                    "descricao": t.descricao,
                    "valor": t.valor,
                    "data": t.data,
                    "tipo": t.tipo,
                    "categoria": t.categoria.nome if t.categoria else None,
                }
                for t in finance_manager.transactions
            ],
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def carregar_dados(self, finance_manager):
        """Carrega dados do ficheiro JSON (se existir) para o finance_manager."""
        if not os.path.exists(self.filename):
            # primeira vez, não há ficheiro -> não faz nada
            return

        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # limpar listas atuais
        finance_manager.users = []
        finance_manager.categories = []
        finance_manager.transactions = []

        # carregar categorias
        categorias_por_nome = {}
        for c in data.get("categories", []):
            cat = Category(c["nome"])
            finance_manager.categories.append(cat)
            categorias_por_nome[c["nome"]] = cat

        # carregar utilizadores
        for u in data.get("users", []):
            user = User(
                id=u["id"],
                nome=u["nome"],
                email=u["email"],
                password=u["password"],
                perfil=u["perfil"],
            )
            finance_manager.users.append(user)

        # carregar transações
        for t in data.get("transactions", []):
            cat = categorias_por_nome.get(t["categoria"])
            trans = Transaction(
                id=t["id"],
                descricao=t["descricao"],
                valor=t["valor"],
                data=t["data"],
                tipo=t["tipo"],
                categoria=cat,
            )
            finance_manager.transactions.append(trans)
