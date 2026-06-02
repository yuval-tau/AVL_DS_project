import matplotlib.pyplot as plt
import random

def draw_tree(tree_input):
    # Extract root
    root = tree_input.get_root() if hasattr(tree_input, 'get_root') else tree_input
    
    if root is None or (hasattr(root, 'is_real_node') and not root.is_real_node()):
        print("Tree is empty.")
        return

    nodes_pos = {}
    edges = []
    x_counter = [0]

    def calculate_positions(node, depth):
        if node is None or (hasattr(node, 'is_real_node') and not node.is_real_node()):
            return
            
        calculate_positions(node.left, depth + 1)
        nodes_pos[node] = (x_counter[0], -depth)
        x_counter[0] += 1
        calculate_positions(node.right, depth + 1)

    def build_edges(node):
        if node is None or (hasattr(node, 'is_real_node') and not node.is_real_node()):
            return
            
        if node.left and (not hasattr(node.left, 'is_real_node') or node.left.is_real_node()):
            edges.append((nodes_pos[node], nodes_pos[node.left]))
            build_edges(node.left)
            
        if node.right and (not hasattr(node.right, 'is_real_node') or node.right.is_real_node()):
            edges.append((nodes_pos[node], nodes_pos[node.right]))
            build_edges(node.right)

    calculate_positions(root, 0)
    build_edges(root)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Draw edges
    for (x1, y1), (x2, y2) in edges:
        ax.plot([x1, x2], [y1, y2], 'k-', lw=1.5, zorder=1)

    # Draw nodes and labels
    for node, (x, y) in nodes_pos.items():
        ax.plot(x, y, 'o', markersize=35, color='lightgreen', markeredgecolor='black', zorder=2)
        
        # Get key and height
        key = str(node.key) if hasattr(node, 'key') else "?"
        h = node.get_height() if hasattr(node, 'get_height') else (node.height if hasattr(node, 'height') else "?")
        
        label = f"{key}\nh:{h}"
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold', zorder=3)

    # Get tree size for title
    tree_size = tree_input.size() if hasattr(tree_input, 'size') else len(nodes_pos)
    
    ax.axis('off')
    plt.title(f"Tree Visualization | Size: {tree_size}", fontsize=16)
    plt.tight_layout()
    plt.show()

# --- Example ---
if __name__ == "__main__":
    from AVLTree import AVLTree
    
    my_tree = AVLTree(is_avl=False)
    for i in range(20):
        num = random.randrange(50)+1
        my_tree.insert(num, str(num))
        
    draw_tree(my_tree)