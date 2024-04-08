from PyQt5.QtCore import Qt, QAbstractTableModel


class UserListModel(QAbstractTableModel):
    def __init__(self, linked_list, headers, parent=None):
        super(UserListModel, self).__init__(parent)
        self.linkedList = linked_list
        self.headers = headers

    def rowCount(self, parent):
        return self.linkedList.countUsers()

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            user = self.linkedList.getUserAtIndex(index.row())
            columnName = self.headers[index.column()]

            if columnName == "Name":
                return user.name
            elif columnName == "Username":
                return user.userName
            elif columnName == "Password":
                return user.password
            elif columnName == "Email":
                return user.email
            elif columnName == "CNIC":
                return user.id
            elif columnName == "Admin":
                return "Yes" if user.isAdmin else "No"
            if not user.isAdmin:
                if columnName == "Staff":
                    return "Yes" if user.isStaff else "No"
            else:
                if columnName == "Staff":
                    return "N/A"
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]

        return None
