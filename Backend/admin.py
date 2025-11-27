from user import User

class Admin(User):
    def __init__(self, id, nome, email, password):
        super().__init__(id, nome, email, password, perfil="admin")

    def gerir_utilizadores(self):
        pass
