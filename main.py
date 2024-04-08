from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
import sys
from BL.member import Member
from BL.admin import Admin
from DL.UserDL import UserDL
from DL.BookDL import BookDL
from BL.book import Book
from Models.issueEventModel import issueEventsModel
from Models.tableModel import booksTableModel
from Models.userListModel import UserListModel
from Models.singleListModel import stackTableModel
from Models.notificationPopup import NotificationPopup
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import traceback
import datetime
import matplotlib.pylab as plt

mainpath = r"D:\DSAFinalProject"


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()

        self.loginUi = mainpath + r"\UI\login.ui"
        self.signupUi = mainpath + r"\UI\signup.ui"
        self.adminUi = mainpath + r"\UI\admin.ui"
        self.memberUi = mainpath + r"\UI\member.ui"
        self.editBookUi = mainpath + r"\UI\editBook.ui"
        self.issueBookUi = mainpath + r"\UI\issueBook.ui"
        self.issueBookMemberUi = mainpath + r"\UI\issueBookMember.ui"
        self.returnBookUi = mainpath + r"\UI\returnBook.ui"
        self.extendBookUi = mainpath + r"\UI\extendBook.ui"
        self.messageDisplayUi = mainpath + r"\UI\message.ui"
        self.historyUi = mainpath + r"\UI\history.ui"

        self.columns = [
            "ISBN",
            "Title",
            "Author",
            "Genre",
            "Issue Status",
            "Issue Date",
            "Return Date",
        ]
        self.userColumns = [
            "Name",
            "Username",
            "Password",
            "Email",
            "CNIC",
            "Admin",
            "Staff",
        ]
        self.notificationColumns = ["Message", "Date", "View Status"]

        self.initialLogin()

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        UserDL.readDataFromFile()
        BookDL.readDataFromFile()
        BookDL.readIssueEventsFromFile()
        BookDL.readHistoryFromFile()
        BookDL.readReservedUsersFromFile()
        BookDL.calculateFine()
        UserDL.readNotificationsFromFile()

        self.books = BookDL.getBooks()
        self.list = UserDL.getUsers()
        self.notification = None
        self.id = None
        self.name = None
        self.username = None
        self.password = None
        self.email = None
        self.currentUser = None

        self.stackedWidget = None

    def center(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def initialLogin(self):
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        loadUi(self.loginUi, self)
        self.center()

        signUp = self.innerWidget.findChild(QtWidgets.QWidget, "signUpBtn")
        signUp.clicked.connect(self.showSignUp)

        loginBtn = self.innerWidget.findChild(QtWidgets.QWidget, "loginBtn")
        loginBtn.clicked.connect(self.loginClicked)

    def showSignUp(self):
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.clearCentralWidget()
        loadUi(self.signupUi, self)
        self.center()

        idWidget = self.innerWidget.findChild(QtWidgets.QWidget, "cnic")
        nameWidget = self.innerWidget.findChild(QtWidgets.QWidget, "name")
        userNameWidget = self.innerWidget.findChild(QtWidgets.QWidget, "userName")
        passwordWidget = self.innerWidget.findChild(QtWidgets.QWidget, "password")
        emailWidget = self.innerWidget.findChild(QtWidgets.QWidget, "email")

        self.inputValidator(idWidget, "id")
        self.inputValidator(nameWidget, "name")

        def signUpClicked():
            try:
                self.id = idWidget.text()
                self.name = nameWidget.text()
                self.userName = userNameWidget.text()
                self.password = passwordWidget.text()
                self.email = emailWidget.text()

                if (
                    self.id
                    and self.name
                    and self.userName
                    and self.password
                    and self.email
                    and self.validationChecker(emailWidget.text(),idWidget.text())
                ):
                    user = Member(
                        self.id, self.name, self.userName, self.password, self.email
                    )
                    if self.list.search(self.userName, self.password) != None:
                        print("Username already exists")
                        self.showNotification("Username already exists")
                    else:
                        self.list.append(user)
                        #self.list.display()
                        print("Signup Successfull")
                        UserDL.writeToFile()
                        self.showNotification("Signup Successfull")
                        self.showLogin()
                else:
                    print("Complete all the entities")
                    self.showNotification("Input is inavalid")
            except Exception as e:
                print(f"Error: {e}")

        backBtn = self.innerWidget.findChild(QtWidgets.QWidget, "backBtn")
        backBtn.clicked.connect(self.showLogin)

        signUp = self.innerWidget.findChild(QtWidgets.QWidget, "signUpBtn")
        signUp.clicked.connect(signUpClicked)

    def showLogin(self):
        try:
            # self.clearCentralWidget()
            loadUi(self.loginUi, self)
            self.center()
            # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

            signUp = self.findChild(QtWidgets.QWidget, "signUpBtn")
            signUp.clicked.connect(self.showSignUp)

            loginBtn = self.findChild(QtWidgets.QWidget, "loginBtn")
            loginBtn.clicked.connect(self.loginClicked)
        except Exception as e:
            print(f"Error: {e}")

    def loginClicked(self):
        usernameWidget = self.innerWidget.findChild(QtWidgets.QWidget, "userName")
        passwordWidget = self.innerWidget.findChild(QtWidgets.QWidget, "password")

        self.username = usernameWidget.text()
        self.password = passwordWidget.text()

        if self.username and self.password:
            self.currentUser = self.list.search(self.username, self.password)
            if self.currentUser != None and self.currentUser.isAdmin:
                self.adminMenu()
            elif self.currentUser != None and not self.currentUser.isAdmin:
                self.readerMenu()
            else:
                print("User not found")
                usernameWidget.setText("")
                passwordWidget.setText("")
                self.showNotification("User not found")
        else:
            self.showNotification("Complete all the entities")

    def clearCentralWidget(self):
        if self.centralWidget():
            self.centralWidget().deleteLater()

    def adminMenu(self):
        try:
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint, False)
            self.clearCentralWidget()
            loadUi(self.adminUi, self)
            self.center()
            # self.showMaximized()

            self.stackedWidget = self.outerWidget.findChild(
                QtWidgets.QWidget, "stackedWidget"
            )
            self.homeBtnClicked()
            btnWidget = self.outerWidget.findChild(
                QtWidgets.QWidget, "leftMenuContainer"
            )

            homeBtn = btnWidget.findChild(QtWidgets.QWidget, "homeBtn")
            homeBtn.clicked.connect(self.homeBtnClicked)

            addBookBtn = btnWidget.findChild(QtWidgets.QWidget, "addBookBtn")
            addBookBtn.clicked.connect(self.addBookClicked)

            manageBtn = btnWidget.findChild(QtWidgets.QWidget, "manageBooksBtn")
            manageBtn.clicked.connect(self.manageBooksClicked)

            myAccountBtn = btnWidget.findChild(QtWidgets.QWidget, "myAccountBtn")
            myAccountBtn.clicked.connect(self.myAccountClicked)

            addUsersBtn = btnWidget.findChild(QtWidgets.QWidget, "addUsersBtn")
            addUsersBtn.clicked.connect(self.addUsersClicked)

            editUsersBtn = btnWidget.findChild(QtWidgets.QWidget, "editUsersBtn")
            editUsersBtn.clicked.connect(self.editUsersClicked)

            logoutBtn = self.widget_13.findChild(QtWidgets.QWidget, "logoutBtn")
            logoutBtn.clicked.connect(self.logout)

            notificationBtn = self.widget_13.findChild(
                QtWidgets.QWidget, "notificationBtn"
            )
            notificationBtn.clicked.connect(lambda: self.notificationMember(6))
        except Exception as e:
            print(f"Error: {e}")

    def logout(self):
        # Close the current dashboard and return to the login screen
        self.clearCentralWidget()
        self.showLogin()

    def homeBtnClicked(self):
        self.stackedWidget.setCurrentIndex(0)
        issueBookLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "issueBooksLbl")
        lateBookLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "lateBookLbl")
        membersLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "membersLbl")
        viewStatsBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "viewStatsBtn")
        issueBookLbl.setText(BookDL.getIssuedBooksCount())
        lateBookLbl.setText(BookDL.countLateBooks())
        membersLbl.setText(UserDL.getMembersCount())
        def viewStats():
            issueCountList = BookDL.getBooksIssueCount()
            booksList = BookDL.getBookTitles()
            plt.bar(booksList, issueCountList)
            plt.xlabel("Books")
            plt.ylabel("Issued Count")
            plt.show()
        viewStatsBtn.clicked.connect(viewStats)



    def addBookClicked(self):
        self.stackedWidget.setCurrentIndex(1)
        mainWidget = self.stackedWidget.findChild(QtWidgets.QWidget, "mainWidget")
        addBtn = mainWidget.findChild(QtWidgets.QWidget, "addBtn")

        def addBtnClicked():
            isbnLbl = mainWidget.findChild(QtWidgets.QWidget, "isbnTxt")
            titleLbl = mainWidget.findChild(QtWidgets.QWidget, "titleTxt")
            autherLbl = mainWidget.findChild(QtWidgets.QWidget, "authorTxt")
            genreLbl = mainWidget.findChild(QtWidgets.QWidget, "genreTxt")

            isbn = isbnLbl.text()
            title = titleLbl.text()
            auther = autherLbl.text()
            genre = genreLbl.text()

            if title and auther and genre and isbn and self.checkValidation(genreLbl.text(),autherLbl.text(),isbnLbl.text()):
                book = Book(isbn, title, auther, genre)
                BookDL.addBook(book)
                BookDL.writeToFile()
                members = UserDL.getSpecificUsers("member")
                for member in members:
                    member.addNotifications(book.addBooknotification())
                UserDL.writeNotificationsToFile()
                isbnLbl.setText("")
                titleLbl.setText("")
                autherLbl.setText("")
                genreLbl.setText("")
                self.showNotification("Book added successfully!")
            else:
                self.showNotification("Input Should be Valid")

        addBtn.clicked.connect(addBtnClicked)
    def checkValidation(self,genre,author,isbn):
            if  isbn.isdigit() and  not genre.isdigit() and  not author.isdigit() and len(isbn)>=10 and len(isbn)<13:
                return True
            else:
                return  False
    def manageBooksClicked(self):
        self.stackedWidget.setCurrentIndex(2)
        book = None
        ascending = self.stackedWidget.findChild(QtWidgets.QWidget, "ascendRBtn")
        descending = self.stackedWidget.findChild(QtWidgets.QWidget, "descendRBtn")

        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView")
        tableView.setModel(booksTableModel(self.books, self.columns))
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        searchTxt = self.stackedWidget.findChild(QtWidgets.QWidget, "searchTxt")
        searchBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "searchBtn")

        def issueBookClicked():
            dlg = QDialog()
            loadUi(self.issueBookUi, dlg)
            selectedRows = self.checkSelectedRow("tableView")
            mainWidget = dlg.findChild(QtWidgets.QWidget, "mainWidget")
            tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView")

            if selectedRows is not None:
                book = BookDL.searchBookByTitle(
                    tableView.model().index(selectedRows, 1).data()
                )
                title = mainWidget.findChild(QtWidgets.QWidget, "bookTitle")
                title.setText(book.title)
                isbn = mainWidget.findChild(QtWidgets.QWidget, "bookISBN")
                isbn.setText(book.isbn)

                def issue():
                    username = mainWidget.findChild(
                        QtWidgets.QWidget, "memberTxt"
                    ).text()
                    if username:
                        user = UserDL.searchUserByUserName(username)
                        if not user.isAdmin:
                            self.issueBookBtnClicked(user, book, dlg)
                        else:
                            self.showNotification("Can't issue book to admin")

                issueBtn = dlg.findChild(QtWidgets.QWidget, "issueBookBtn")
                issueBtn.clicked.connect(issue)
                dlg.exec_()
            else:
                self.showNotification("Select a Book")

        def historyBtnClicked():
            dlg = QDialog()
            loadUi(self.historyUi, dlg)
            selectedRows = self.checkSelectedRow("tableView")
            tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView")
            if selectedRows is not None:
                book = BookDL.searchBookByTitle(
                    tableView.model().index(selectedRows, 1).data()
                )
                historyView = dlg.findChild(QtWidgets.QWidget, "historyView")
                historyView.setModel(issueEventsModel(book.history))
                dlg.exec_()
            else:
                self.showNotification("Select one row")

        def setModel(list):
            tableView.setModel(
                booksTableModel(
                    list, self.columns, True if descending.isChecked() else False
                )
            )

        def search():
            searchQuery = searchTxt.text()
            books = BookDL.searchBook(searchQuery)
            setModel(books)

        setModel(self.books)

        editBookBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "editBookBtn")
        editBookBtn.clicked.connect(self.editBookClicked)

        issueBookBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "issueBookBtn")
        issueBookBtn.clicked.connect(issueBookClicked)

        historyBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "historyBtn")
        historyBtn.clicked.connect(historyBtnClicked)
        
        ascending.clicked.connect(lambda: setModel(self.books))
        descending.clicked.connect(lambda: setModel(self.books))

        searchBtn.clicked.connect(search)

    def checkSelectedRow(self, table):
        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, table)
        selectionModel = tableView.selectionModel()
        selectedIndexes = selectionModel.selectedIndexes()
        selectedRows = list(set(index.row() for index in selectedIndexes))
        if selectedRows:
            return selectedRows[0]
        else:
            return None

    def editBookClicked(self):
        dlg = QDialog()
        loadUi(self.editBookUi, dlg)
        selectedRows = self.checkSelectedRow("tableView")
        mainWidget = dlg.findChild(QtWidgets.QWidget, "mainWidget")
        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        def deleteBookBtn(title):
            book = BookDL.searchBookByTitle(title.text())
            BookDL.deleteBook(title.text())
            BookDL.writeToFile()
            members = UserDL.getSpecificUsers("member")
            for member in members:
                member.addNotifications(book.removeBooknotification())
            UserDL.writeNotificationsToFile()
            dlg.close()
            tableView.setModel(booksTableModel(self.books, self.columns))
            self.showNotification("Book deleted sucessfully")

        def saveBookBtn(isbn, title, author, genre):
            book = BookDL.searchBookByTitle(title.text())
            book.isbn = isbn.text()
            book.title = title.text()
            book.author = author.text()
            book.genre = genre.text()
            if  self.checkValidation(genre.text(),author.text(),isbn.text()):
                BookDL.writeToFile()
                dlg.close()
            else:
                self.showNotification('invalid Input')

        if selectedRows:
            title = mainWidget.findChild(QtWidgets.QWidget, "titleTxt")
            auther = mainWidget.findChild(QtWidgets.QWidget, "authorTxt")
            genre = mainWidget.findChild(QtWidgets.QWidget, "genreTxt")
            isbn = mainWidget.findChild(QtWidgets.QWidget, "isbnTxt")
            deleteBtn = mainWidget.findChild(QtWidgets.QWidget, "deleteBtn")
            saveBtn = mainWidget.findChild(QtWidgets.QWidget, "saveBtn")
            isbn.insert(tableView.model().index(selectedRows, 0).data())
            title.insert(tableView.model().index(selectedRows, 1).data())
            auther.insert(tableView.model().index(selectedRows, 2).data())
            genre.insert(tableView.model().index(selectedRows, 3).data())
            deleteBtn.clicked.connect(lambda: deleteBookBtn(title))
            saveBtn.clicked.connect(lambda: saveBookBtn(isbn, title, auther, genre))
        dlg.exec_()

    def addUsersClicked(self):
        self.stackedWidget.setCurrentIndex(3)
        mainWidget = self.stackedWidget.findChild(QtWidgets.QWidget, "widget_10")
        nameLbl = mainWidget.findChild(QtWidgets.QWidget, "nameInput")
        usernameLbl = mainWidget.findChild(QtWidgets.QWidget, "usernameInput")
        passwordLbl = mainWidget.findChild(QtWidgets.QWidget, "passwordInput")
        emailLbl = mainWidget.findChild(QtWidgets.QWidget, "emailInput")
        cnicLbl = mainWidget.findChild(QtWidgets.QWidget, "cnicInput")
        adminRBtn = mainWidget.findChild(QtWidgets.QWidget, "adminRBtn_2")
        staffRBtn = mainWidget.findChild(QtWidgets.QWidget, "staffRBtn_2")
        memberRBtn = mainWidget.findChild(QtWidgets.QWidget, "memberRBtn_2")

        self.inputValidator(cnicLbl, "id")
        self.inputValidator(nameLbl, "name")

        def clearAll():
            nameLbl.setText("")
            usernameLbl.setText("")
            passwordLbl.setText("")
            emailLbl.setText("")
            cnicLbl.setText("")
            adminRBtn.setChecked(False)
            staffRBtn.setChecked(False)
            memberRBtn.setChecked(False)

        def addUser():
            admin, staff = False, False
            
            if (
                nameLbl.text()
                and usernameLbl.text()
                and passwordLbl.text()
                and emailLbl.text()
                and cnicLbl.text()
                and self.validationChecker(emailLbl.text(),cnicLbl.text())
            ):
                if adminRBtn.isChecked():
                    admin = True
                    user = Admin(
                        cnicLbl.text(),
                        nameLbl.text(),
                        usernameLbl.text(),
                        passwordLbl.text(),
                        emailLbl.text(),
                        admin,
                    )
                else:
                    if staffRBtn.isChecked():
                        staff = True
                    user = Member(
                        cnicLbl.text(),
                        nameLbl.text(),
                        usernameLbl.text(),
                        passwordLbl.text(),
                        emailLbl.text(),
                        staff,
                    )

                self.list.append(user)
                UserDL.writeToFile()
                self.showNotification("User added successfully!")
                clearAll()

            else:
            
                self.showNotification("Input Should be Valid ")

        addUserBtn = mainWidget.findChild(QtWidgets.QWidget, "addUserBtn")
        addUserBtn.clicked.connect(addUser)
    def validationChecker(self,email,cnic):
            print(email,cnic)
            if cnic.isdigit() and len(cnic) == 13 and "@" in email  and  email.endswith(".com") :
                return True
            else:
                return False
    def myAccountClicked(self):
        self.stackedWidget.setCurrentIndex(5)

        nameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "nameLbl")
        nameLbl.insert(self.currentUser.name)

        usernameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "usernameLbl")
        usernameLbl.insert(self.currentUser.userName)

        passwordLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "passwordLbl")
        passwordLbl.insert(self.currentUser.password)

        saveBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "saveBtn")
        saveBtn.clicked.connect(self.saveBtnClicked)

    def saveBtnClicked(self):
        nameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "nameLbl")
        self.currentUser.name = nameLbl.text()

        usernameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "usernameLbl")
        self.currentUser.userName = usernameLbl.text()

        passwordLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "passwordLbl")
        self.currentUser.password = passwordLbl.text()

        UserDL.writeToFile()

        self.showNotification("User details updated successfully!")

    def editUsersClicked(self):
        self.stackedWidget.setCurrentIndex(4)
        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView2")

        def selectedUserChanged():
            tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView2")
            selectedIndexes = tableView.selectedIndexes()

            if selectedIndexes:
                selectedRow = selectedIndexes[0].row()
                nameTxt.setText(str(tableView.model().index(selectedRow, 0).data()))
                cnicTxt.setText(str(tableView.model().index(selectedRow, 4).data()))
                emailTxt.setText(str(tableView.model().index(selectedRow, 3).data()))
                usernameTxt.setText(str(tableView.model().index(selectedRow, 1).data()))
                passwordTxt.setText(str(tableView.model().index(selectedRow, 2).data()))

                if tableView.model().index(selectedRow, 5).data() == "Yes":
                    adminRBtn.setChecked(True)
                else:
                    adminRBtn.setChecked(False)
                    if tableView.model().index(selectedRow, 6).data() == "Yes":
                        staffRBtn.setChecked(True)
                    else:
                        staffRBtn.setChecked(False)
                        memberRBtn.setChecked(True)

        def setTableModel(list=self.list):
            tableView.setModel(UserListModel(list, self.userColumns))
            selectionModel = tableView.selectionModel()
            selectionModel.selectionChanged.connect(selectedUserChanged)

        def setModel():
            if rB1.isChecked():
                setTableModel()
            elif rB2.isChecked():
                list = self.list.getUserByRole("admin")
                setTableModel(list)
            elif rB3.isChecked():
                list = self.list.getUserByRole("staff")
                setTableModel(list)
            elif rB4.isChecked():
                list = self.list.getUserByRole("member")
                setTableModel(list)

        mainWidget = self.stackedWidget.findChild(QtWidgets.QWidget, "mainWidget_4")
        searchTxt = self.stackedWidget.findChild(QtWidgets.QWidget, "searchBarTxt")
        rB1 = self.stackedWidget.findChild(QtWidgets.QWidget, "allUsersRBtn")
        rB2 = self.stackedWidget.findChild(QtWidgets.QWidget, "adminUserRBtn")
        rB3 = self.stackedWidget.findChild(QtWidgets.QWidget, "staffUserRBtn")
        rB4 = self.stackedWidget.findChild(QtWidgets.QWidget, "memberUserRBtn")
        nameTxt = mainWidget.findChild(QtWidgets.QWidget, "nameTxt")
        cnicTxt = mainWidget.findChild(QtWidgets.QWidget, "cnicTxt")
        emailTxt = mainWidget.findChild(QtWidgets.QWidget, "emailTxt")
        usernameTxt = mainWidget.findChild(QtWidgets.QWidget, "userNameTxt")
        passwordTxt = mainWidget.findChild(QtWidgets.QWidget, "passwordTxt")
        adminRBtn = mainWidget.findChild(QtWidgets.QWidget, "adminRBtn")
        memberRBtn = mainWidget.findChild(QtWidgets.QWidget, "memberRBtn")
        staffRBtn = mainWidget.findChild(QtWidgets.QWidget, "staffRBtn")

        searchBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "searchBtn_2")
        saveBtn = mainWidget.findChild(QtWidgets.QWidget, "saveBtn_2")
        deleteBtn = mainWidget.findChild(QtWidgets.QWidget, "deleteBtn")

        def clearAll():
            nameTxt.setText("")
            cnicTxt.setText("")
            emailTxt.setText("")
            usernameTxt.setText("")
            passwordTxt.setText("")
            adminRBtn.setChecked(False)
            staffRBtn.setChecked(False)
            memberRBtn.setChecked(False)

        def saveBtnClicked():
            if usernameTxt.text():
                user = self.list.search(usernameTxt.text(), passwordTxt.text())
                user.name = nameTxt.text()
                user.cnic = cnicTxt.text()
                user.email = emailTxt.text()
                user.username = usernameTxt.text()
                user.password = passwordTxt.text()
                user.isAdmin = adminRBtn.isChecked()
                if not user.isAdmin:
                    user.isStaff = staffRBtn.isChecked()
                    setModel()
                UserDL.writeToFile()
                clearAll()
                self.showNotification("User details updated successfully!")
            else:
                self.showNotification("Select one Row")

        def deleteBtnClicked():
            user = self.list.search(usernameTxt.text(), passwordTxt.text())
            if user:
                UserDL.deleteUser(user.userName)
                UserDL.writeToFile()

                setModel()
                clearAll()
                self.showNotification("User deleted successfully!")

        def search():
            text = searchTxt.text()
            if text:
                list = self.list.getUserByName(text)
                setTableModel(list)
            pass

        setModel()

        rB1.clicked.connect(setModel)
        rB2.clicked.connect(setModel)
        rB3.clicked.connect(setModel)
        rB4.clicked.connect(setModel)

        searchBtn.clicked.connect(search)
        saveBtn.clicked.connect(saveBtnClicked)
        deleteBtn.clicked.connect(deleteBtnClicked)

    def showNotification(self, message):
        notification = NotificationPopup("Notification", message, self)
        notification.exec_()

    def addReminder(self):
        books = self.currentUser.myBooks
        for book in books:
            if datetime.date.today() == book.issueEvent.returnDate:
                self.currentUser.addNotifications(book.generateReturnReminder())
                UserDL.writeNotificationsToFile()

    def addLateReminder(self):
        books = self.currentUser.myBooks
        for book in books:
            if datetime.date.today() > book.issueEvent.returnDate:
                self.currentUser.addNotifications(book.generateLateNotification())
                UserDL.writeNotificationsToFile()

    def readerMenu(self):
        try:
            BookDL.calculateFine()

            self.setWindowFlag(QtCore.Qt.FramelessWindowHint, False)
            self.clearCentralWidget()
            loadUi(self.memberUi, self)
            self.center()
            # self.showMaximized()
            self.addReminder()
            self.addLateReminder()
            self.stackedWidget = self.widget.findChild(
                QtWidgets.QWidget, "stackedWidget"
            )
            self.stackedWidget.setCurrentIndex(0)
            btnWidget = self.widget.findChild(QtWidgets.QWidget, "leftMenuContainer")

            myBooksbtn = btnWidget.findChild(QtWidgets.QWidget, "myBookBtn")
            myBooksbtn.clicked.connect(self.myBooksMember)

            viewBooksBtn = btnWidget.findChild(QtWidgets.QWidget, "viewBtn")
            viewBooksBtn.clicked.connect(self.viewBooksMember)

            homeBtn = btnWidget.findChild(QtWidgets.QWidget, "homeBtn")
            homeBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

            myAccountBtn = btnWidget.findChild(QtWidgets.QWidget, "myAccountBtn")
            myAccountBtn.clicked.connect(self.myAccountMember)

            notificationBtn = self.widget_12.findChild(
                QtWidgets.QWidget, "notificationBtn"
            )
            notificationBtn.clicked.connect(lambda: self.notificationMember(4))

            logoutBtn = self.widget_12.findChild(QtWidgets.QWidget, "logoutBtn")
            logoutBtn.clicked.connect(self.logout)

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def myBooksMember(self):
        try:
            self.stackedWidget.setCurrentIndex(2)

            issuedRBtn = self.stackedWidget.findChild(
                QtWidgets.QWidget, "issuedBooksRBtn"
            )
            reservedRBtn = self.stackedWidget.findChild(
                QtWidgets.QWidget, "reservedBooksRBtn"
            )

            tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView_2")
            tableView.setModel(booksTableModel(self.currentUser.myBooks, self.columns))
            self.tableView_2.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch
            )

            def setTableModel(list=self.currentUser.myBooks):
                columns = self.columns.copy()
                columns.pop(4)
                tableView.setModel(booksTableModel(list, columns, False, True))

            def setModel():
                if issuedRBtn.isChecked():
                    setTableModel()
                elif reservedRBtn.isChecked():
                    list = BookDL.getReservedBooks(self.currentUser)
                    setTableModel(list)

            def returnBook():
                if issuedRBtn.isChecked():
                    selectedRows = self.checkSelectedRow("tableView_2")
                    if selectedRows is not None:
                        book = BookDL.searchBookByTitle(
                            tableView.model().index(selectedRows, 1).data()
                        )
                        self.currentUser.returnBook(book.title)
                        admins = UserDL.getSpecificUsers("admin")
                        for admin in admins:
                            admin.addNotifications(
                                book.returnBooknotification(self.currentUser)
                            )
                        UserDL.writeNotificationsToFile()
                        self.showNotification("Book returned successfully!")
                        book.returnBook()
                        BookDL.writeIssueEventsToFile()
                        BookDL.writeHistoryToFile()
                        tableView.setModel(
                            booksTableModel(self.currentUser.myBooks, self.columns)
                        )

            def extendBookMemeber():
                if issuedRBtn.isChecked():
                    selectedRows = self.checkSelectedRow("tableView_2")
                    dlg = QDialog()
                    loadUi(self.extendBookUi, dlg)

                    if selectedRows is not None:
                        days = dlg.findChild(QtWidgets.QWidget, "days").text()
                        book = BookDL.searchBookByTitle(
                            tableView.model().index(selectedRows, 1).data()
                        )
                        extendBook = dlg.findChild(QtWidgets.QWidget, "extendBook")

                        def extendBookBtn(days):
                            book.extendBook(days)
                            self.showNotification("Book extended successfully!")
                            dlg.close()

                        extendBook.clicked.connect(lambda: extendBookBtn(int(days)))
                        dlg.exec_()

            setModel()

            issuedRBtn.clicked.connect(setModel)
            reservedRBtn.clicked.connect(setModel)

            returnBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "returnBtn")
            returnBtn.clicked.connect(returnBook)

            extendBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "extendBtn")
            extendBtn.clicked.connect(extendBookMemeber)

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def viewBooksMember(self):
        self.stackedWidget.setCurrentIndex(1)
        book = None
        ascending = self.stackedWidget.findChild(QtWidgets.QWidget, "ascendRBtn")
        descending = self.stackedWidget.findChild(QtWidgets.QWidget, "descendRBtn")

        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        searchTxt = self.stackedWidget.findChild(QtWidgets.QWidget, "searchTxt")
        searchBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "searchBtn")
        reserveBookBtn = self.stackedWidget.findChild(
            QtWidgets.QWidget, "reserveBookBtn"
        )

        def setModel(list):
            tableView.setModel(
                booksTableModel(
                    list, self.columns, True if descending.isChecked() else False
                )
            )

        def reserveBookBtnClicked(member):
            selectedRows = self.checkSelectedRow("tableView")
            if selectedRows is not None:
                book = BookDL.searchBookByTitle(
                    tableView.model().index(selectedRows, 1).data()
                )
                if not book.isIssued:
                    flag = book.reserve(member)
                    if flag:
                        BookDL.writeReservedUsersToFile()
                        self.showNotification("Book reserved successfully!")
                    else:
                        self.showNotification("Can't reserve Book. It is reserved!")
                else:
                    self.showNotification("Can't reserve Book. It is issued!")
            else:
                self.showNotification("Select one Row")

        def issueBookMember():
            try:
                selectedRows = self.checkSelectedRow("tableView")
                dlg = QDialog()
                loadUi(self.issueBookMemberUi, dlg)
                mainWidget = dlg.findChild(QtWidgets.QWidget, "mainWidget")
                if selectedRows is not None:
                    book = BookDL.searchBookByTitle(
                        tableView.model().index(selectedRows, 1).data()
                    )
                    titleLbl = mainWidget.findChild(QtWidgets.QWidget, "titleLbl")
                    titleLbl.setText(book.title)

                    issueBookBtn = mainWidget.findChild(
                        QtWidgets.QWidget, "issueBookBtn"
                    )

                    issueBookBtn.clicked.connect(
                        lambda: self.issueBookBtnClicked(self.currentUser, book, dlg)
                    )
                    dlg.exec_()

                else:
                    self.showNotification("Select one Row")

            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()

        def search():
            searchQuery = searchTxt.text()
            books = BookDL.searchBook(searchQuery)
            setModel(books)

        setModel(self.books)

        reserveBookBtn.clicked.connect(lambda: reserveBookBtnClicked(self.currentUser))
        ascending.clicked.connect(lambda: setModel(self.books))
        descending.clicked.connect(lambda: setModel(self.books))

        issueBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "issueBtn")
        issueBtn.clicked.connect(issueBookMember)

        searchBtn.clicked.connect(search)

    def issueBookBtnClicked(self, member, book, dlg):
        if not book.isIssued:
            flag = book.issueBook(member)
            if flag:
                self.showNotification("Book issued successfully!")
                member.addMyBooks(book)
                admins = UserDL.getSpecificUsers("admin")
                for admin in admins:
                    admin.addNotifications(book.issueBooknotification(self.currentUser))
                UserDL.writeNotificationsToFile()
                BookDL.writeIssueEventsToFile()
            else:
                self.showNotification("Can't issue Book. It is reserved!")
        else:
            self.showNotification("Book already issued!")
        dlg.close()

    def myAccountMember(self):
        self.stackedWidget.setCurrentIndex(3)
        nameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "nameLbl")
        self.inputValidator(nameLbl, "name")
        nameLbl.insert(self.currentUser.name)

        usernameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "usernameLbl")
        usernameLbl.insert(self.currentUser.userName)

        passwordLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "passwordLbl")
        passwordLbl.insert(self.currentUser.password)

        emailLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "emailLbl")
        emailLbl.insert(self.currentUser.email)

        fineLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "fineLbl")
        fineLbl.insert(str(self.currentUser.fine) + " Rs")
        fineLbl.setEnabled(False)
        def saveBtnClicked():
            nameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "nameLbl")
            self.currentUser.name = nameLbl.text()

            usernameLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "usernameLbl")
            self.currentUser.userName = usernameLbl.text()

            passwordLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "passwordLbl")
            self.currentUser.password = passwordLbl.text()
            
            emailLbl = self.stackedWidget.findChild(QtWidgets.QWidget, "emailLbl")
            self.currentUser.email =emailLbl.text()
            
            if "@"  in emailLbl.text() and  emailLbl.text().endswith(".com"):
                UserDL.writeToFile()
                self.showNotification("User details updated successfully!")
            else:
                self.showNotification('Invalid email')

        
        saveBtn = self.stackedWidget.findChild(QtWidgets.QWidget, "saveBtn")
        saveBtn.clicked.connect(saveBtnClicked)

    def notificationMember(self, pageNumber):
        self.stackedWidget.setCurrentIndex(pageNumber)
        tableView = self.stackedWidget.findChild(QtWidgets.QWidget, "tableView_3")
        self.tableView_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableView.setModel(
            stackTableModel(self.currentUser.notifications, self.notificationColumns)
        )

        def showMessage():
            selectedRows = self.checkSelectedRow("tableView_3")
            dlg = QDialog()
            loadUi(self.messageDisplayUi, dlg)
            if selectedRows is not None:
                textbrowser = dlg.findChild(QtWidgets.QWidget, "textBrowser")
                textbrowser.append(tableView.model().index(selectedRows, 0).data())
                notification = self.currentUser.searchNotification(
                    tableView.model().index(selectedRows, 0).data()
                )
                notification.isViewed = True
                UserDL.writeNotificationsToFile()
                dlg.exec_()
            else:
                self.showNotification("Select one Row")

        openMessageBtn = self.stackedWidget.findChild(
            QtWidgets.QWidget, "openMessageBtn"
        )
        openMessageBtn.clicked.connect(showMessage)

    def inputValidator(self, widget, type):
        if type == "id":
            validator = QRegExpValidator(QRegExp("[0-9]+"))
        elif type == "name":
            validator = QRegExpValidator(QRegExp("[a-zA-Z\s]+"))
        widget.setValidator(validator)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())
