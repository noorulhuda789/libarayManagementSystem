class Node:
    def __init__(self, user):
        self.user = user
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, user):
        newNode = Node(user)
        if not self.head:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

    def search(self, username, password):
        current = self.head
        while current:
            if current.user.userName == username and current.user.password == password:
                return current.user
            current = current.next
        return None

    def searchByUsername(self, username):
        current = self.head
        while current:
            if current.user.userName == username:
                return current.user
            current = current.next
        return None

    def delete(self, username):
        current = self.head
        while current:
            if current.user.userName == username:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev

                return True
            current = current.next
        return False

    def countUsers(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def getUserAtIndex(self, index):
        count = 0
        current = self.head
        while current:
            if count == index:
                return current.user
            count += 1
            current = current.next
        return None

    def getUserByName(self, name):
        users = DoublyLinkedList()
        current = self.head
        while current:
            if name in current.user.name:
                users.append(current.user)
            current = current.next
        return users

    def getUserByRole(self, role):
        users = DoublyLinkedList()
        current = self.head
        while current:
            if role == "admin":
                if current.user.isAdmin:
                    users.append(current.user)
            elif role == "staff":
                if not current.user.isAdmin and current.user.isStaff:
                    users.append(current.user)
            elif role == "member":
                if not current.user.isAdmin and not current.user.isStaff:
                    users.append(current.user)
            current = current.next
        return users

    def __iter__(self):
        current = self.head
        while current:
            yield current.user
            current = current.next

    def display(self):
        current = self.head
        while current:
            print(current.user)
            current = current.next
