from collections.abc import Container, Sized


class ListNode:
    def __init__(self, parent, value, prev=None, next=None):
        self._parent = None
        self._value = value

        self.parent = parent
        self.prev = prev
        self.next = next

        self.parent.index(self)

    def __repr__(self):
        return repr(self.value)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if self._parent != None:
            self._parent.unindex(self)

        self._parent = parent

        if self._parent != None:
            self._parent.index(self)

    @property
    def value(self):
        return self._value

    def push(self, value):
        n = ListNode(self.parent, value)

        n.prev, self.next, n.next = self, n, self.next

        return n

    def pop(self):
        if self.next == None:
            return None

        n = self.next

        self.next = n.next
        if self.next != None:
            self.next.prev = self

        n.next = None
        n.prev = None
        n.parent = None

        return n

    def insert(self, head, tail):
        n = head
        while n != None:
            n.parent = self.parent
            n = n.next

        head.prev = self
        tail.next = self.next

        if self.next != None:
            self.next.prev = tail

        self.next = head

    def remove(self, count):
        head, tail = self.next, self.next

        for _ in range(count - 1):
            if tail.next != None:
                tail = tail.next

        if tail.next != None:
            tail.next.prev, self.next = self, tail.next

        head.prev = None
        tail.next = None

        return DoubleLinkedList(head=head, tail=tail)


class DoubleLinkedList(Container, Sized):
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self._index = dict()

        n = head
        while n != None:
            n.parent = self
            n = n.next

    def __contains__(self, item):
        return item in self._index

    def __len__(self):
        return len(self._index)

    def __repr__(self):
        return f"head: {repr(self.head)}, tail: {repr(self.tail)}, len: {len(self)}"

    def index(self, node):
        self._index[node.value] = node

    def unindex(self, node):
        self._index.pop(node.value, None)

    def find(self, value):
        return self._index[value]