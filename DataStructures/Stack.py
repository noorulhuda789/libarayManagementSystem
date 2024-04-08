class Stack:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def push(self, data):
        self._items.insert(0, data)

    def pop(self):
        if not self.isEmpty():
            return self._items.pop(0)
        else:
            print("stack underflow")
            return None

    def isEmpty(self):
        return len(self._items) == 0

    def top(self):
        if not self.isEmpty():
            return self._items[0]
        else:
            print("the stack is empty")
            return None

    def count(self):
        return len(self._items)

    def change(self, p, val):
        if 0 <= p < len(self._items):
            self._items[p] = val
            print(f"the element has been changed at position {p}: {val}")
        else:
            print("invalid position")

    def __iter__(self):
        return iter(self._items)

    def display(self):
        if not self.isEmpty():
            print("the stack elements are:", end=" ")
            for item in reversed(self._items):
                print(item, end=" ")
            print()
        else:
            print("the stack is empty")
