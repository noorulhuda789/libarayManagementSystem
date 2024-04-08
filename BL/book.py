from BL.issueEvent import IssueEvent
from DataStructures.PriorityQueue import PriorityQueue
from BL.notifications import Notifications
from DataStructures import Stack


class Book:
    def __init__(self, isbn, title, author, genre, isIssued=False):
        self._isbn = isbn
        self._title = title
        self._author = author
        self._genre = genre
        self._isIssued = isIssued
        self._issueEvent = None
        self._reservedUsers = PriorityQueue()
        self._history = []

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        self._isbn = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def reservedUsers(self):
        return self._reservedUsers

    @reservedUsers.setter
    def reservedUsers(self, value):
        self._reservedUsers = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def isIssued(self):
        return self._isIssued

    @isIssued.setter
    def isIssued(self, value):
        self._isIssued = value

    @property
    def issueEvent(self):
        return self._issueEvent

    @issueEvent.setter
    def issueEvent(self, value):
        self._issueEvent = value

    @property
    def history(self):
        return self._history
    
    def historyCount(self):
        return len(self._history)

    def addHistory(self, history):
        self._history.append(history)

    def reserve(self, user):
        if not self._reservedUsers.search(user):
            self._reservedUsers.push(user)
            return True
        else:
            return False

    def unreserve(self, user):
        self._reservedUsers.pop(user)

    def issueBook(self, member):
        if self.reservedUsers.isEmpty():
            self._isIssued = True
            self._issueEvent = IssueEvent(member, self)
            return True
        else:
            if self.reservedUsers.top() == member:
                self._reservedUsers.pop()
                self._isIssued = True
                self._issueEvent = IssueEvent(member, self)
                return True
            else:
                return False

    def returnBook(self):
        self._isIssued = False
        self.addHistory(self._issueEvent)
        self._issueEvent = None

    def extendBook(self, days):
        self._issueEvent.extendReturnDate(days)

    def issueBooknotification(self, member):
        return Notifications(
            f"The member {member.name} has issued this book {self._title}."
        )

    def returnBooknotification(self, member):
        return Notifications(
            f"The member {member.name} has returned this book {self._title}."
        )

    def reservedBooknotification(self, member):
        return Notifications(
            f"The member {member.name} has reserved this book {self._title}."
        )

    def addBooknotification(self):
        return Notifications(f"This book {self._title} is added in the library.")

    def removeBooknotification(self):
        return Notifications(f"This book {self._title} is removed from the library.")

    def reserveBooknotification(self):
        return Notifications(
            f"This book {self._title} is reserved by the member {self._reservedUsers.top().name}."
        )

    def generateReturnReminder(self):
        return Notifications(
            f"It's time to return your book {self.title}. Return it soon otherwise you will be fined."
        )

    def generateLateNotification(self):
        return Notifications(
            f"You are late to return your book {self.title}. You are being fined."
        )

    def writeHistoryToFile(self):
        return "\n".join([history.writeToFile() for history in self.history])

    def writeReservedUsersToFile(self):
        return ",".join([user.userName for user in self.reservedUsers.queue])

    def writeToFile(self):
        return f"{self._isbn}|{self._title}|{self._author}|{self._genre}|{int(self._isIssued)}"

    def __str__(self):
        return f"ISBN: {self._isbn}\n Title: {self._title}\n Author: {self._author}\n Genre: {self._genre}\n isIssued: {self._isIssued}"
