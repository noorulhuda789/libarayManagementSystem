from DataStructures.LinkedList import DoublyLinkedList
from BL.admin import Admin
from BL.member import Member
from BL.notifications import Notifications
import datetime


class UserDL:
    _users = DoublyLinkedList()

    @staticmethod
    def getUsers():
        return UserDL._users

    @staticmethod
    def addUser(user):
        UserDL._users.append(user)

    @staticmethod
    def searchUserByUserName(username):
        return UserDL._users.searchByUsername(username)

    @staticmethod
    def deleteUser(username):
        return UserDL._users.delete(username)

    @staticmethod
    def searchUser(username, password):
        return UserDL._users.search(username, password)

    @staticmethod
    def getSpecificUsers(role):
        return UserDL._users.getUserByRole(role)

    @staticmethod
    def displayList():
        UserDL._users.display()

    @staticmethod
    def getMembersCount():
        count = 0
        for user in UserDL._users:
            if not user.isAdmin :
                count+=1
        return str(count)
    
  


    @staticmethod
    def getNotification():
        return UserDL._notifications

    @staticmethod
    def addNotification(notification):
        UserDL._notifications.push(notification)

    @staticmethod
    def readDataFromFile():
        lines = None
        with open("membersData.csv", mode="r") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                user = None
                temp = None
                if line == "":
                    continue
                line = line.replace("\n", "")
                line = line.split(",")

                user = None
                if bool(int(line[5])):
                    user = Admin(line[0], line[1], line[2], line[3], line[4], True)
                else:
                    user = Member(
                        line[0],
                        line[1],
                        line[2],
                        line[3],
                        line[4],
                        bool(int(line[5])),
                        bool(int(line[6])),
                        int(line[7]),
                    )
                UserDL.addUser(user)

    @staticmethod
    def writeToFile():
        with open("membersData.csv", mode="w") as file:
            for user in UserDL._users:
                file.write(user.writeToFile() + "\n")

    @staticmethod
    def readNotificationsFromFile():
        lines = None
        with open("notifications.csv", mode="r") as file:
            lines = file.readlines()
        if lines:
            for line in lines:
                if line == "":
                    continue
                line = line.replace("\n", "")
                notifs = line.split("|")
                user = UserDL.searchUserByUserName(notifs[0])
                for notif in reversed(notifs[1:]):
                    notif = notif.split(",")
                    notification = Notifications(
                        notif[0],
                        bool(int(notif[1])),
                        datetime.datetime.strptime(notif[2], "%Y-%m-%d").date(),
                    )
                    user.addNotifications(notification)

    @staticmethod
    def writeNotificationsToFile():
        with open("notifications.csv", mode="w") as file:
            for user in UserDL._users:
                if not user.notifications.isEmpty():
                    file.write(
                        user.userName + "|" + user.writeNotifications() + "\n"
                    )
