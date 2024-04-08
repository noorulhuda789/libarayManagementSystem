from PyQt5.QtCore import QObject, Qt, QAbstractTableModel

class stackTableModel(QAbstractTableModel):
    def __init__(self, Stack, columns, parent=None):
        super().__init__(parent)
        self.Stack = Stack
        self.columns = columns

    def rowCount(self, parent=None): 
        return self.Stack.count()

    def columnCount(self, parent=None):
        return len(self.columns)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            stack = self.Stack.items[index.row()]

            if index.column() == 0:
                return stack.message
            elif index.column() == 1:
                
                return stack.date.strftime("%d/%m/%Y")
            elif index.column() == 2:
                if not stack.isViewed:
                   
                    return "UnRead"
                else:
                    return "Read"
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]
        return None
