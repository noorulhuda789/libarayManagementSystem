from BL.notifications import Notifications
from DataStructures.Stack import Stack  


class User:
    def __init__(self, id, name, userName, password, email, isAdmin):
        self._id = id
        self._name = name
        self._userName = userName
        self._password = password
        self._email = email
        self._isAdmin = isAdmin
        self._notifications = Stack()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, value):
        self._userName = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def isAdmin(self):
        return self._isAdmin

    @isAdmin.setter
    def isAdmin(self, value):
        self._isAdmin = value

    @property
    def notifications(self):
        return self._notifications

    def addNotifications(self, notification: Notifications):
        self._notifications.push(notification)

    def searchNotification(self, message):
        anotherStack = Stack()
        for i in range(self.notifications.count()):
            if (self.notifications.top().message == message):
                notification = self.notifications.pop()
                anotherStack.push(notification)
            else:
                anotherStack.push(self.notifications.pop())
        for i in range(anotherStack.count()):
            self.notifications.push(anotherStack.pop())
        return notification
        

    def writeNotifications(self):
        return "|".join(
            [notification.writeToFile() for notification in self.notifications]
        )

    def writeToFile(self):
        return f"{self.id},{self.name},{self.userName},{self.password},{self.email}"

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\nUsername: {self.userName}\nIs Admin: {self.isAdmin}\n"
        )
