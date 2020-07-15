class Node:
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next = next_node

    def __repr__(self):
        return str(self.element)


class Stack:
    def __init__(self):
        self.head = Node()

    def is_empty(self):
        return self.head.next is None

    def push(self, element):
        self.head.next = Node(element, self.head.next)

    def pop(self):
        node = self.head.next
        if not self.is_empty():
            self.head.next = node.next
        return node


def test():
    stack = Stack()
    stack.push(0)
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)

    print(stack.pop())


if __name__ == "__main__":
    test()