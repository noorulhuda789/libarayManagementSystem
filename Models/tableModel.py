from PyQt5.QtCore import Qt, QAbstractTableModel


class booksTableModel(QAbstractTableModel):
    def __init__(self, bst, columns, reversed=False, isMyBooks=False, parent=None):
        super().__init__(parent)
        if reversed:
            self.bst = bst.inOrder()[::-1]
        else:
            self.bst = bst.inOrder()
        if isMyBooks:
            self.columnHeaders = columns
        else:
            self.columnHeaders = columns[:5]
        self.isMyBooks = isMyBooks

    def rowCount(self, parent=None):
        return len(self.bst) if self.bst else 0

    def columnCount(self, parent=None):
        return len(self.columnHeaders) if self.columnHeaders else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            lst = self.bst
            book = lst[index.row()]
            if index.column() == 0:
                return book.isbn
            elif index.column() == 1:
                return book.title
            elif index.column() == 2:
                return book.author
            elif index.column() == 3:
                return book.genre
            if not self.isMyBooks:
                if index.column() == 4:
                    return "Yes" if book.isIssued else "No"
            else:
                if book.issueEvent:
                    if index.column() == 4:
                        return book.issueEvent.issueDate.strftime("%d-%m-%Y")
                    elif index.column() == 5:
                        return book.issueEvent.returnDate.strftime("%d-%m-%Y")
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return (
                self.columnHeaders[section]
                if section < len(self.columnHeaders)
                else None
            )
        return None
