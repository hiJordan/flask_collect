class Node(object):
    def __init__(self, element=-1):
        self.element = element
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        index = 0
        node = self.head
        while node is not None:
            index += 1
            node = node.next
        return index

    def find(self, element):
        node = self.head
        while node is not None:
            if node.element == element:
                break
            node = node.next
        return node

    def _node_at_index(self, index):
        i = 0
        node = self.head
        while node is not None:
            if i == index:
                break
            node = node.next
            i += 1
        return node

    def element_at_index(self, index):
        node = self._node_at_index(index)
        return node.element

    def insert_before_index(self, position, element):
        current_node = Node(element)
        before_node = self.head
        index = 0
        if position == 0:
            current_node.next = before_node
            self.head = current_node
            return

        while before_node is not None:
            if index == position - 1:
                break
            index += 1
            before_node = before_node.next
        before_node.next = current_node
        current_node.next = self._node_at_index(position)

    def insert_after_index(self, position, element):
        current_node = Node(element)
        before_node = self._node_at_index(position)
        after_node = before_node.next
        before_node.next = current_node
        current_node.next = after_node

    def first_object(self):
        return self.head

    def last_object(self):
        last_index = self.length() - 1
        return self._node_at_index(last_index)

    def append(self, node):
        if self.head is None:
            self.head = node
        else:
            before_node = self.last_object()
            before_node.next = node
        # self.log_linked(self.head)

    def log_linked(self, head_node):
        node = head_node
        linked_element = []
        while node is not None:
            linked_element.append(node.element)
            node = node.next
        print(linked_element)


def test():
    node = Node(1)
    linked = LinkedList()
    linked.append(node)
    linked.append(Node(2))
    linked.append(Node(3))

    linked.log_linked(linked.head)
    linked.log_linked(linked.last_object())
    linked.log_linked(linked.first_object())
    linked.insert_after_index(2, 4)
    linked.log_linked(linked.head)
    linked.insert_before_index(0, 0)
    linked.log_linked(linked.head)
    print(linked.element_at_index(2))
    print(linked.length())


if __name__ == '__main__':
    test()