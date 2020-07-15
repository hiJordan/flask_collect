class Tree:
    def __init__(self, element=None):
        self.element = element
        self.left = None
        self.right = None

    def traversal(self):
        # 前序遍历
        print(self.element)
        if self.left is not None:
            self.left.traversal()
        # 中序遍历 print(self.element)
        if self.right is not None:
            self.right.traversal()
        # 后序遍历 print(self.element)

    def reverse(self):
        self.left, self.right = self.right, self.left
        if self.left is not None:
            self.left.reverse()
        if self.right is not None:
            self.right.reverse()


def test():
    t = Tree(0)
    t.left = Tree(1)
    t.right = Tree(2)
    t.traversal()

    t.reverse()
    t.traversal()


if __name__ == "__main__":
    test()