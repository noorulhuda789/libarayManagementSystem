class PriorityQueue:
    def __init__(self):
        self._queue = []

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value):
        self._queue = value

    def push(self, user):
        index = self.insertionIndex(user.isStaff)
        self._queue.insert(index, user)

    def pop(self):
        if self._queue:
            return self._queue.pop(0)
        else:
            raise IndexError("pop from an empty priority queue")

    # def pop(self, user):
    #     if self._queue:
    #         return self._queue.remove(user)
    #     else:
    #         raise IndexError("pop from an empty priority queue")

    def search(self, user):
        return True if user in self._queue else False

    def top(self):
        return self._queue[0]

    def isEmpty(self):
        return len(self._queue) == 0

    def insertionIndex(self, isStaff):
        for i, r in enumerate(self._queue):
            if isStaff and not r.isStaff:
                return i
        return len(self._queue)

    def display(self):
        if not self.isEmpty():
            print([user.userName for user in self._queue])
        else:
            print("the queue is empty")
