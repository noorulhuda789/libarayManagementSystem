import datetime


class IssueEvent:
    def __init__(
        self,
        member,
        book,
        issueDate=datetime.date.today(),
        returnDate=datetime.date.today() + datetime.timedelta(days=7),
    ):
        self._member = member
        self._book = book
        self._issueDate = issueDate
        self._returnDate = returnDate

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._member = value

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        self._book = value

    @property
    def issueDate(self):
        return self._issueDate

    @issueDate.setter
    def issueDate(self, value):
        self._issueDate = value

    @property
    def returnDate(self):
        return self._returnDate

    @returnDate.setter
    def returnDate(self, value):
        self._returnDate = value

    def extendReturnDate(self, days):
        self.returnDate += datetime.timedelta(days=days)

    def writeToFile(self):
        return f"{self.member.userName}|{self.book.title}|{self.issueDate}|{self.returnDate}"

    def __str__(self):
        return f"Member: {self.member.name}\tBook: {self.book.title}\tIssue Date: {self.issueDate}\tReturn Date: {self.returnDate}"
