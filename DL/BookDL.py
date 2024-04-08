from DataStructures.BinarySearchTree import BinarySearchTree
from BL.book import Book
from BL.issueEvent import IssueEvent
from DL.UserDL import UserDL
import datetime


class BookDL:
    _books = BinarySearchTree()

    @staticmethod
    def getBooks():
        return BookDL._books

    @staticmethod
    def addBook(book):
        BookDL._books.insert(book)

    @staticmethod
    def deleteBook(title):
        BookDL._books.delete(title)

    @staticmethod
    def searchBook(title):
        return BookDL._books.search(title)

    @staticmethod
    def searchBookByTitle(title):
        return BookDL._books.search(title).root.data

    @staticmethod
    def getIssuedBooksCount():
        count = 0
        for book in BookDL._books.preOrder():
            if book.issueEvent:
                count += 1
        return str(count)

    @staticmethod
    def getBookTitles():
        list = []
        for book in BookDL._books.preOrder():
            list.append(book.title)
        return list

    @staticmethod
    def countLateBooks():
        count = 0
        for book in BookDL._books.preOrder():
            if book.issueEvent and book.issueEvent.returnDate < datetime.date.today():
                count += 1
        return str(count)

    @staticmethod
    def getBooksIssueCount():
        list = []
        for book in BookDL._books.preOrder():
            list.append(book.historyCount())
        return list

    @staticmethod
    def getReservedBooks(user):
        reservedBooks = BinarySearchTree()
        for book in BookDL._books.preOrder():
            if not book.reservedUsers.isEmpty() and book.reservedUsers.search(user):
                reservedBooks.insert(book)
        return reservedBooks

    @staticmethod
    def calculateFine():
        for book in BookDL._books.preOrder():
            if book.issueEvent:
                if book.issueEvent.returnDate < datetime.date.today():
                    user = book.issueEvent.member
                    daysLate = (datetime.date.today() - book.issueEvent.returnDate).days
                    fine = 100 * daysLate
                    user.addFine(fine)

    @staticmethod
    def displayList():
        BookDL._books.display()

    @staticmethod
    def readDataFromFile():
        lines = None
        with open(r"books.csv", mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                line = line.split("|")
                book = Book(
                    line[0],
                    line[1],
                    line[2],
                    line[3],
                    bool(int(line[4].replace("\n", ""))),
                )
                BookDL.addBook(book)

    @staticmethod
    def writeToFile():
        with open(r"books.csv", mode="w") as file:
            books = BookDL._books.preOrder()
            for book in books:
                file.write(book.writeToFile() + "\n")

    @staticmethod
    def readIssueEventsFromFile():
        lines = None
        with open(r"issueEvents.csv", mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                if line=="":
                    continue
                line = line.split("|")
                book = BookDL.searchBookByTitle(line[1])
                user = UserDL.searchUserByUserName(line[0])
                book.issueEvent = IssueEvent(
                    user,
                    book,
                    datetime.datetime.strptime(line[2], "%Y-%m-%d").date(),
                    datetime.datetime.strptime(
                        line[3].replace("\n", ""), "%Y-%m-%d"
                    ).date(),
                )
                book.isIssued = True
                user.addMyBooks(book)

    @staticmethod
    def writeIssueEventsToFile():
        with open(r"issueEvents.csv", mode="w") as file:
            books = BookDL._books.preOrder()
            for book in books:
                if book.issueEvent:
                    file.write(book.issueEvent.writeToFile() + "\n")

    @staticmethod
    def readHistoryFromFile():
        lines = None
        with open(r"issueEventsHistory.csv", mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                line = line.split(",")
                book = BookDL.searchBookByTitle(line[1])
                user = UserDL.searchUserByUserName(line[0])
                book.history.append(
                    IssueEvent(
                        user,
                        book,
                        datetime.datetime.strptime(line[2], "%Y-%m-%d").date(),
                        datetime.datetime.strptime(
                            line[3].replace("\n", ""), "%Y-%m-%d"
                        ).date(),
                    )
                )

    @staticmethod
    def writeHistoryToFile():
        with open(r"issueEventsHistory.csv", mode="w") as file:
            books = BookDL._books.preOrder()
            for book in books:
                if book.history:
                    file.write(book.writeHistoryToFile() + "\n")

    @staticmethod
    def readReservedUsersFromFile():
        lines = None
        with open(r"reservedUsers.csv", mode="r", encoding="utf-8-sig") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                if line == "":
                    continue
                line = line.split("|")
                book = BookDL.searchBookByTitle(line[0])
                queue = []
                for userName in line[1].split(","):
                    queue.append(
                        UserDL.searchUserByUserName(userName.replace("\n", ""))
                    )
                book.reservedUsers.queue = queue

    @staticmethod
    def writeReservedUsersToFile():
        with open(r"reservedUsers.csv", mode="w") as file:
            books = BookDL._books.preOrder()
            for book in books:
                if not book.reservedUsers.isEmpty():
                    file.write(
                        book.title + "|" + book.writeReservedUsersToFile() + "\n"
                    )
