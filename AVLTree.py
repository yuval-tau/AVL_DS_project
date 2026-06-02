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

    def __init__(self, key, value, left=None, right=None, parent=None, is_real=True):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.height = -1
        self.is_real = is_real


    def is_real_node(self):
        """returns whether self is not a virtual node 
        @rtype: bool
        @returns: False if self is a virtual node, True otherwise.
        """
        return self.is_real
    

    def is_leaf(self):
        """returns whether self is a leaf node (i.e. both children are virtual nodes)

        @rtype: bool
        @returns: True if self is a leaf node, False otherwise. virtual nodes aren't leaf nodes.
        """
        if not self.is_real_node():
            return False
        return  self.left.is_real_node() and self.right.is_real_node()


    def get_height(self):
        """Return the stored height of the node.

        Height convention:
        - A virtual node has height -1.
        - A real leaf has height 0.
        - A real internal node has height 1 + max(height(left), height(right)).
        The height field should be updated explicitly after structural changes.
        """
        return self.height

    def set_height(self, height):
        """Set the stored height of the node.
        
        @param height: the new height value to store in the node
        @type height: int
        """
        self.height = height




class AVLTree(object):

# Tree invariants:
# - An empty tree has root = None and tree_size = 0.
# - Each AVLTree object owns exactly one shared virtual node.
# - Every real leaf points to this shared virtual node as both left and right child.
# - The shared virtual node has height -1 and is_real = False.
# - Real nodes should be created only through create_real_node().
# - We do not set parent for the shared virtual node, because it is shared by many leaves.





    def __init__(self, is_avl = False):
        """
        Constructor, you are allowed to add more fields.

        @type is_avl: boolean
        @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
        """
        self.root = None
        self.tree_size = 0
        self.is_avl = is_avl
        

       ###creation of The only Virtual Node
        self.virtual_node = AVLNode(None, None,is_real=False)
        self.virtual_node.height = -1
   

    def update_height(self, node):
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
        if node is not None and node.is_real_node():
            node.set_height( 1 + max(node.left.get_height(), node.right.get_height()))
    

    def search(self, key):
        """searches for a node in the dictionary corresponding to the key (starting at the root)

        @type key: int
        @param key: a key to be searched
        @rtype: (AVLNode,int)
        @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
        and search_time is the search time, as defined and explained in the assignment.
        """
        search_time = 1
        curr = self.root

        if not curr.is_real_node():
            return None, search_time

        while curr.is_real_node():
            search_time += 1
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return curr, search_time
        search_time += 1
        return None, search_time



    def insert(self, key, val):
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

        search_time = 1
        rotations = 0
        height_changes = 0
        curr = self.root
        new_node = AVLNode(key, val, left=self.virtual_node, right=self.virtual_node, parent=None)

        if curr is None:
            print("inserting root")
            self.root = new_node
            print(f"added node with key {new_node.key} and value {new_node.value}")
            self.tree_size += 1
            return new_node, search_time, rotations, height_changes

        while not curr.is_leaf():
            search_time += 1
            if key < curr.key:
                curr = curr.left
            else: 
                curr = curr.right
        #reached a leaf, insert the new node as a child of curr
        search_time += 1
        self.set_parent(curr, new_node)
        if key < curr.key:
            curr.left = new_node
        else:
            curr.right = new_node
        self.tree_size += 1
        return new_node, search_time, rotations, height_changes        

    def get_successor(self, node):
        """returns the successor of node in the in-order traversal of the tree

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        @rtype: AVLNode or None
        @returns: the successor of node, or None if node has no successor (i.e. node is the maximum)
        """
        if node is None or not node.is_real_node():
            return None

        #case 1: node has a right child, successor is the leftmost descendant of the right child
        if node.right.is_real_node():
            curr = node.right
            while curr.left.is_real_node():
                curr = curr.left
            return curr

        #case 2: node has no right child, successor is the lowest ancestor of node whose left child is also an ancestor of node
        curr = node
        while curr.parent is not None and curr.parent.right == curr:
            curr = curr.parent
        return curr.parent

    def delete(self, node):

        """deletes node from the dictionary

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        """
        if node is None or not node.is_real_node():
            return

        #case 1: node is a leaf
        if node.is_leaf():
            if node == self.root:
                self.root = None
            else:
                parent = node.parent
                if parent.left == node:
                    parent.left = self.virtual_node
                else:
                    parent.right = self.virtual_node
            self.tree_size -= 1
            return

        #counting the number of children to determine which case we are in
        child_count = 1
        if node.left.is_real_node() and node.right.is_real_node():
            child_count = 2
        
        #case 2: node has exactly one child, we bypass node and connect its parent directly to its child
        if child_count == 1:
            child = node.left if node.left.is_real_node() else node.right
            if node == self.root:
                self.root = child
                self.set_parent(child, None)
            else:
                parent = node.parent
                if parent.left == node:
                    parent.left = child
                else:
                    parent.right = child
                self.set_parent(child, parent)
            self.tree_size -= 1

        #case 3: node has two children, we replace node with its successor and then delete the successor (which is guaranteed to have at most one child)
        else:
            successor = self.get_successor(node)
            node.key = successor.key
            node.value = successor.value
            self.delete(successor)
            self.tree_size -= 1
        return
        


    def avl_to_list(self):

        """returns a list representing dictionary 

        @rtype: list
        @returns: a list of (key, value) tuples sorted by key, representing the data structure
        """
        result = []

        def inorder(node):
            if node is None or not node.is_real_node():
                return

            inorder(node.left)
            result.append((node.key, node.value))
            inorder(node.right)

        inorder(self.root)
        return result
    



    def size(self):
        """returns the number of items in dictionary

        @rtype: int
        @returns: the number of items in dictionary 
        """
        return self.tree_size


    def get_root(self):
        """returns the root of the tree representing the dictionary

        @rtype: AVLNode
        @returns: the root, None if the dictionary is empty
        """

        return self.root


    def get_height(self):
        """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """
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
        


    def set_left(self, parent, child):
        """Set the left child of a given parent node.

        Assigns child as the left child of parent. 
        If child is a real node, its parent pointer is also updated.
        @param parent: the node whose left child is being set
        @type parent: AVLNode
        @param child: the node to set as the left child of parent
        @type child: AVLNode or None
        """
        parent.left = child
        if child is not None and child.is_real_node():
            child.parent = parent
    
    def get_left(self, node):
        """Return the left child of node."""
        return node.left

   

    def set_right(self, parent, child):
        """Set the right child of a given parent node.

        This method assigns child as the right child of parent.
        If child is a real node, its parent pointer is also updated to parent.
        Virtual nodes are not assigned a parent because the virtual node is shared.

        @param parent: the node whose right child is being set
        @type parent: AVLNode
        @param child: the node to set as the right child of parent
        @type child: AVLNode or None
        """
        parent.right = child
        if child is not None and child.is_real_node():
            child.parent = parent

    
    def get_right(self, node):
        """Return the right child of node."""
        return node.right
    

    def set_parent(self, current_node, parent_node):
        """set the parent of a given node
        
        @param current_node: the node whose parent we want to set
        @type current_node: AVLNode
        @param parent_node: the node that we want to be the parent of current_node.
                            Can be None if current_node is the root.
        @type parent_node: AVLNode or None
        """
        if current_node is not None and current_node.is_real_node():
            current_node.parent = parent_node


    def get_parent(self, node):
        """Return the parent of node."""
        return node.parent

   