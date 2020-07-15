class Node:
    def __init__(self, element=None, next_node=None):
        self.element = element
        self.next = next_node

    def __repr__(self):
        return str(self.element)


class Queue:
    def __init__(self):
        self.head = Node()
        self.tail = self.head

    def is_empty(self):
        return self.head.next is None

    def enqueue(self, element):
        node = Node(element)
        self.tail.next = node
        self.tail = node

    def dequeue(self):
        node = self.head.next
        if not self.is_empty():
            self.head.next = node.next
        return node


def test():
    queue = Queue()
    queue.enqueue(0)
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    queue.enqueue(4)
    print(queue.dequeue())
    print(queue.dequeue())


if __name__ == "__main__":
    test()
