# id1:212204291
# name1:Ziv Karari
# username1:zivkarari
# id2:
# name2:Yuval Samocha
# username2:


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.is_real = False

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.is_real



    """Return the stored height of the node.

    Height convention:
    - A virtual node has height -1.
    - A real leaf has height 0.
    - A real internal node has height 1 + max(height(left), height(right)).
    The height field should be updated explicitly after structural changes.
    """
    def get_height(self):
        return self.height


    """Set the stored height of the node.

    @param height: the new height value to store in the node
    @type height: int
    """
    def set_height(self, height):
        self.height = height




    




"""
A class implementing an AVL tree.
"""


class AVLTree(object):

# Tree invariants:
# - An empty tree has root = None and tree_size = 0.
# - Each AVLTree object owns exactly one shared virtual node.
# - Every real leaf points to this shared virtual node as both left and right child.
# - The shared virtual node has height -1 and is_real = False.
# - Real nodes should be created only through create_real_node().
# - We do not set parent for the shared virtual node, because it is shared by many leaves.



    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.root = None
        self.tree_size = 0
        self.is_avl = is_avl
        

       ###creation of The only Virtual Node
        self.virtual_node = AVLNode(None, None)
        self.virtual_node.is_real = False
        self.virtual_node.height = -1

    """returns new default node
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: AVLNode
    @returns: the new node we just created
    """
    def create_real_node(self, key, value): ###create a real node NOT virtual
        node = AVLNode(key, value)
        node.is_real = True
        node.height = 0
        node.left = self.virtual_node
        node.right = self.virtual_node
        node.parent = None
        return node
    


    
   
    """Update the stored height of a real node according to its children.

    Height convention:
    - A virtual node always has height -1.
    - A real leaf has height 0.
    - A real internal node has height 1 + max(height(left), height(right)).
    - In an AVL tree, the tree height is the stored height of the root.
    - In a regular BST, the tree height may be computed recursively.

    AVLNode.get_height() only returns the stored value.
    After structural changes in an AVL tree, such as insert, delete, or rotation,
    the heights of the affected real nodes must be updated explicitly.

    @param node: the node whose height should be updated
    @type node: AVLNode
    """
    def update_height(self, node):
        if node is not None and node.is_real_node():
            node.set_height( 1 + max(node.left.get_height(), node.right.get_height()))
    

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        return None, -1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        return None, -1, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def delete(self, node):
        return

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        result = []

        def inorder(node):
            if node is None or not node.is_real_node():
                return

            inorder(node.left)
            result.append((node.key, node.value))
            inorder(node.right)

        inorder(self.root)
        return result
    

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.tree_size

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """
    def get_height(self):
        if self.root is None:
            return -1
        if self.is_avl:
            return self.root.get_height()
        return self.compute_height(self.root)
    
    def compute_height(self, node):
        if node is None or not node.is_real_node():
            return -1

        return 1 + max(
            self.compute_height(node.left),
            self.compute_height(node.right)
        )
        

    """Set the left child of a given parent node.
     Assigns child as the left child of parent. 
     If child is a real node, its parent pointer is also updated.
     @param parent: the node whose left child is being set
     @type parent: AVLNode
     @param child: the node to set as the left child of parent
     @type child: AVLNode or None
       """
    def set_left(self, parent, child):
        parent.left = child
        if child is not None and child.is_real_node():
            child.parent = parent
    
    def get_left(self, node):
        return node.left

   
    """Set the right child of a given parent node.

    This method assigns child as the right child of parent.
    If child is a real node, its parent pointer is also updated to parent.
    Virtual nodes are not assigned a parent because the virtual node is shared.

    @param parent: the node whose right child is being set
    @type parent: AVLNode
    @param child: the node to set as the right child of parent
    @type child: AVLNode or None
    """
    def set_right(self, parent, child):
        parent.right = child
        if child is not None and child.is_real_node():
            child.parent = parent

    
    def get_right(self, node):
        return node.right
    
    """set the parent of a given node
    @param current_node: the node whose parent we want to set
    @type current_node: AVLNode
    @param parent_node: the node that we want to be the parent of current_node.
                        Can be None if current_node is the root.
    @type parent_node: AVLNode or None
    """
    def set_parent(self, current_node, parent_node):
        if current_node is not None and current_node.is_real_node():
            current_node.parent = parent_node


    def get_parent(self, node):
        return node.parent

   