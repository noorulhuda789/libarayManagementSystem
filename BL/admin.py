from BL.user import User


class Admin(User):
    def __init__(
        self, id, name, userName, password, email, isAdmin=True
    ):
        super().__init__(id, name, userName, password, email, isAdmin)

    def writeToFile(self):
        return f"{super().writeToFile()},{int(super().isAdmin)}"
