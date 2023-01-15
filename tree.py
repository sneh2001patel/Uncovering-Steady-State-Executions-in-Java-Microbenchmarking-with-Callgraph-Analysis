class CustomNode:
    def __init__(self, parent, val, idx=0):
        self.parent = parent
        self.val = val
        self.index = idx
        self.children = []

    def __str__(self, level=0):
        ret = "----" * level + repr(self.val) + "\n |"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
    
    def change_idx(self, idx):
      self.index = idx

    def add_child(self, child):
        self.children.append(child)


class Edge:
    def __init__(self, parent, child, val):
        self.parent = parent
        self.child = child
        self.val = val

    def chng_val(self, val):
        self.val = val


class Tree:
    def __init__(self, node):
        self.root = node
        self.index_inc = 1 
        self.edges = []

    def get_child(self, parent_node, child_val):

        children = parent_node.children

        for child in children:
            if child.val == child_val:
                return child
        return None

    def add_node(self, parent, new_node):
        new_node.change_idx(self.index_inc)
        print(new_node.index)
        parent.add_child(new_node)
        e = Edge(parent, new_node, 100)
        self.edges.append(e)
        self.index_inc += 1