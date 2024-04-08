class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0
        self.threshold = 0.7  # Load factor threshold for rehashing

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def _hash_function(self, key):
        sum = 0
        for ch in key:
            sum += ord(ch)
        return sum % self.size

    def _rehash(self):
        self.size *= 2
        oldTable = self.table
        self.table = [None] * self.size
        self.count = 0

        for item in oldTable:
            if item:
                for book in item:
                    self.insert(book)

    def insert(self, book):
        if self.count / self.size > self.threshold:
            self._rehash()

        index = self._hash_function(book.isbn)
        if not self.table[index]:
            self.table[index] = []
        self.table[index].append(book)
        self.count += 1

    def remove(self, isbn):
        index = self._hash_function(isbn)
        if self.table[index]:
            for i, user in enumerate(self.table[index]):
                if user.userName == isbn:
                    del self.table[index][i]
                    self.count -= 1
                    return
        print(f"Book '{isbn}' not found.")

    def getBook(self, isbn):
        index = self._hash_function(isbn)
        if self.table[index]:
            for user in self.table[index]:
                if user.userName == isbn:
                    return user
        return None

    def getBookAtIndex(self, index):
        for item in self.table:
            if item:
                for book in item:
                    if index == 0:
                        return book
                    index -= 1
        return None

    def search(self, isbn):
        index = self._hash_function(isbn)
        if self.table[index]:
            for user in self.table[index]:
                if user.isbn == isbn:
                    return user
        return None

    def display(self):
        for i, item in enumerate(self.table):
            if item:
                print(f"Index {i}: {item}")

    def displayTable(self):
        for i, item in enumerate(self.table):
            print(f"Index {i}: {item}")
