from PyQt5.QtCore import Qt, QAbstractTableModel

class issueEventsModel(QAbstractTableModel):
    def __init__(self, events, columns=['Username','Issue Date', 'Return Date'], parent=None):
        super().__init__(parent)
        self.events = events
        self.columnHeaders = columns
    
    def rowCount(self, parent=None):
        return len(self.events) if self.events else 0
    
    def columnCount(self, parent=None):
        return len(self.columnHeaders) if self.columnHeaders else 0
    
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            lst = self.events
            event = lst[index.row()]
            if index.column() == 0:
                return event.member.userName
            elif index.column() == 1:
                return event.issueDate.strftime("%d-%m-%Y")
            elif index.column() == 2:
                return event.returnDate.strftime("%d-%m-%Y")
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return (
                self.columnHeaders[section]
                if section < len(self.columnHeaders)
                else None
            )
        return None