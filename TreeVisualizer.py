import matplotlib.pyplot as plt
from AVLTree import AVLTree, AVLNode

class TreeVisualizer(AVLTree):

# A class that extends AVLTree and visualizes it using matplotlib
# Using insert and delete functions to update the visualization after each operation

    def __init__(self, is_avl = False):
        super().__init__(is_avl)
        self.virtual_node = NodeVisualizer(None, None)
        self.virtual_node.is_real = False
        self.virtual_node.height = -1
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()


    @classmethod
    def from_tree(cls, tree):
        visualizer = cls(tree)
        visualizer.build_graph()
        return visualizer
    

    def insert(self, key, value):
        super().insert(key, value)
        self.build_graph()
        
    def delete(self, key):
        node = self.search(key)
        if node is not None:
            super().delete(node)
        self.build_graph()
    
    def build_graph(self):
        self.ax.clear()
        self._draw_tree(self.root, 0, 0, 1)

    
    def show(self):
        self.ax.clear()
        self._draw_tree(self.root, 0, 0, 1)
        plt.show()


class NodeVisualizer(AVLNode):


    def __init__(self, key, value):

        super().__init__(key, value)
        self.x = 0
        self.y = 0



