from BL.user import User
from DataStructures.BinarySearchTree import BinarySearchTree
from DataStructures.PriorityQueue import PriorityQueue


class Member(User):
    def __init__(
        self, id, name, userName, password, email, isAdmin=False, isStaff=False, fine=0
    ):
        super().__init__(id, name, userName, password, email, isAdmin)
        self._isStaff = isStaff
        self._myBooks = BinarySearchTree()
        self._fine = fine

    @property
    def isStaff(self):
        return self._isStaff

    @isStaff.setter
    def isStaff(self, value):
        self._isStaff = value

    @property
    def fine(self):
        return self._fine

    @fine.setter
    def fine(self, value):
        self._fine = value

    @property
    def myBooks(self):
        return self._myBooks

    def addFine(self, fine):
        self._fine += fine

    def payFine(self, fine):
        self._fine -= fine

    def addMyBooks(self, book):
        self._myBooks.insert(book)

    def returnBook(self, book):
        self._myBooks.delete(book)

    def writeToFile(self):
        return f"{super().writeToFile()},{int(super().isAdmin)},{int(self.isStaff)},{self.fine}"

    def __str__(self) -> str:
        return f"{super().__str__()}ID: {self.id}\n isStaff: {self.isStaff}\n"
