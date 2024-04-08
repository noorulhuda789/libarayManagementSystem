class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def insert(self, book):
        if self._root is None:
            self._root = Node(book)
        else:
            self._insertRecursive(book, self._root)

    def _insertRecursive(self, book, currentNode):
        if book.title < currentNode.data.title:
            if currentNode.left is None:
                currentNode.left = Node(book)
            else:
                self._insertRecursive(book, currentNode.left)
        elif book.title > currentNode.data.title:
            if currentNode.right is None:
                currentNode.right = Node(book)
            else:
                self._insertRecursive(book, currentNode.right)
        else:
            print("Book already exists")

    def delete(self, title):
        self._root = self._deleteRecursive(title, self._root)

    def _deleteRecursive(self, title, currentNode):
        if currentNode is None:
            return currentNode

        if title < currentNode.data.title:
            currentNode.left = self._deleteRecursive(title, currentNode.left)
        elif title > currentNode.data.title:
            currentNode.right = self._deleteRecursive(title, currentNode.right)
        else:
            if currentNode.left is None:
                temp = currentNode.right
                currentNode = None
                return temp
            elif currentNode.right is None:
                temp = currentNode.left
                currentNode = None
                return temp

            temp = self._findMin(currentNode.right)
            currentNode.data = temp.data
            currentNode.right = self._deleteRecursive(
                temp.data.title, currentNode.right
            )

        return currentNode

    def _findMin(self, currentNode):
        if currentNode.left is None:
            return currentNode
        else:
            return self._findMin(currentNode.left)

    def search(self, query):
        if not query:
            return None
        result = BinarySearchTree()
        self._searchRecursive(query.lower(), self._root, result)
        return result

    def _searchRecursive(self, query, currentNode, result):
        if currentNode is None:
            return

        if query in currentNode.data.title.lower():
            result.insert(currentNode.data)

        if query < currentNode.data.title.lower():
            self._searchRecursive(query, currentNode.left, result)

        self._searchRecursive(query, currentNode.right, result)

    def preOrder(self):
        result = []
        if self.root is None:
            print("Tree is empty")
        else:
            self._preOrderRecursive(self.root, result)
        return result

    def _preOrderRecursive(self, currentNode, result):
        if currentNode:
            result.append(currentNode.data)
            self._preOrderRecursive(currentNode.left, result)
            self._preOrderRecursive(currentNode.right, result)

    def inOrder(self):
        result = []
        if self._root is None:
            # print("Tree is empty")
            pass
        else:
            self._inOrderRecursive(self._root, result)
        return result

    def _inOrderRecursive(self, currentNode, result):
        if currentNode:
            self._inOrderRecursive(currentNode.left, result)
            result.append(currentNode.data)
            self._inOrderRecursive(currentNode.right, result)

    def display(self):
        if self._root is None:
            print("Tree is empty")
        else:
            self._displayInOrder(self._root)

    def _displayInOrder(self, currentNode):
        if currentNode is not None:
            self._displayInOrder(currentNode.left)
            print(currentNode.data)
            self._displayInOrder(currentNode.right)

    def __iter__(self):
        return self.inOrder().__iter__()
