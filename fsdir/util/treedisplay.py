import os


class Node(object):
    def __init__(self, name):
        self.name = name
        self.isdir = False
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def display(self, spacing=0):
        indicator = '-' if not self.isdir else '+'

        print "{0}{1}".format(spacing * ' ' + indicator + ' ', self.name)

        for node in self.nodes:
            node.display(spacing + 2)


def _make_tree(tree):
    for file_path in os.listdir(tree.name):
        file_path = os.path.join(tree.name, file_path)

        sub_node = Node(file_path)
        tree.add_node(sub_node)

        if os.path.isdir(file_path):
            sub_node.isdir = True
            _make_tree(sub_node)

    return tree


def display(directory):
    if not os.path.isdir(directory):
        raise ValueError("%s not a directory." % directory)

    root = Node(directory)
    root.isdir = True

    tree = _make_tree(root)

    tree.display()
