"""
Group Name: TERRA

Group Members:  Göktuğ Öztürkcan
                Ibrahim Eren Tilla
                Emre Orta
                Mehmet Bora Kurucu
                İsmail Yavuzselim Taşçı

Programming Language: Python 3

In our program, we implemented alpha beta pruning and minmimaxing algorithms and tested them for the test cases given in the homework documentation.

"""

"""
====================== HOW TO RUN THE CODE ======================
-Make sure you have python installed in your environment.
-Paste the following command into your terminal: python main.py
"""

class Node:
    """
    A class used to create the puzzle and keep it's attributes.

    Methods
    ---------
    __str__()
      Prints the nodes on each level of the tree the depth of the nodes are indicated with "--------" at each level. The longer the line is the deeper the node is in the tree.
    form_tree()
      Forms the tree using the values and assigning the leftmost value to the leftmost leaf and the rightmost value to the rightmost leaf.
    minimax()
      Performs minimax algorithm to the tree.
    alphabeta()
      Performs alphabeta pruning to the tree.
    """
    def __init__(self, value=None, left=None, mid=None, right=None, name=None):
        """
        Parameters
        ----------
        value : int
          The value of node.
        left : Node 
          Left node of the node
        right: Node 
          Right node of the node
        mid : Node 
          Middle node of the node   
        """
        self.left = left
        self.mid = mid
        self.right = right
        self.value = value
        self.name = name
        self.children = [self.left, self.mid, self.right]

    def __str__(self, row=0):
        """
        Taken from:
        https://stackoverflow.com/questions/20242479/printing-a-tree-data-structure-in-python
        Prints the nodes on each level of the tree the depth of the nodes are indicated with "--------" at each level. The longer the line is the deeper the node is in the tree.
        """
        string = "----------" * row + str(self.value or 'None') + "\n"
        for child in self.children:
            if child is not None:
                string += child.__str__(row + 1)
        return string


def form_tree(values):
    """
    Forms the tree using the values taken in left to right order. Where the leftmost value is the leftmost leaf and the rightmost value is the rightmost leaf.
    """
    # the tree structure is set and we accept 9 values
    assert len(values) == 9
    # form the tree
    root = Node(left=Node(left=Node(values[0], name='A'), mid=Node(values[1], name='B'), right=Node(values[2], name='C')),
                mid=Node(left=Node(values[3], name='D'), mid=Node(values[4], name='E'), right=Node(values[5], name='F')),
                right=Node(left=Node(values[6], name='G'), mid=Node(values[7], name='H'), right=Node(values[8], name='I')))

    return root


def minimax(current_node: Node, depth, is_maximizing_player, tracing_enabled):
    """
    minimax algorithm first checks if a level is minimizer or maximizer and if it is a minimizer gets the minimum value to the upper node and if it is maximizing level gets the maximum value out of the three nodes to the upper level.
    """
    if depth == 0:
        return current_node.value

    if is_maximizing_player:
        max_val = float('-inf') # alpha = -infinity
        counter =0
        for child in current_node.children:
            val = minimax(child, depth - 1, False, tracing_enabled)
            max_val = max(max_val, val)
            if max_val == val:
              pathCounter = counter
            counter=counter+1
        current_node.value = max_val
        if tracing_enabled:
            print(f'New value set: {current_node.value}')
            print(str(root))
        if depth==2:
          if (pathCounter==0):
            print("Player choice: L")
          if (pathCounter==1):
            print("Player choice: M")
          if (pathCounter==2):
            print("Player choice: R")  
        return max_val

    else:
        min_val = float('inf') # beta = infinity
        counter =0
        for child in current_node.children:
            val = minimax(child, depth - 1, True, tracing_enabled)
            min_val = min(min_val, val)
            if min_val == val:
              pathCounter = counter
            counter=counter+1
        current_node.value = min_val
        if tracing_enabled:
            print(f'New value set: {current_node.value}')
            print(str(root))
        if depth==2:#should choose last depth
          if (pathCounter==0):
            print("Player choice: L")
          if (pathCounter==1):
            print("Player choice: M")
          if (pathCounter==2):
            print("Player choice: R")
        return min_val

pruned_nodes = []
def alphabeta(current_node: Node, depth, alpha, beta, is_maximizing_player, tracing_enabled):
    """
    alphabeta pruning checks if a leaf node's value is worth checking by anticipating the next move of the minimizer/maximizer. If not it skips that value and moves the maximum/minimum node to the upper level.
    """
    if depth == 0:
        return current_node.value

    if is_maximizing_player:
        max_val = float('-inf') # alpha = -infinity
        counter=0
        for i, child in enumerate(current_node.children):
            val = alphabeta(child, depth - 1, alpha, beta, False, tracing_enabled)
            max_val = max(max_val, val)
            if (val==max_val):
              totalCounter=counter
            alpha = max(alpha, val)
            counter=counter+1
            if beta <= alpha:
                if tracing_enabled:
                    print(f'Pruning after processing {child.value}')
                for j, child in enumerate(current_node.children):
                    if j > i:
                        pruned_nodes.append(child)
                break

        current_node.value = max_val
        if tracing_enabled:
            print(f'New value set: {current_node.value}')
            print(str(root))
        if depth==2:
          if (totalCounter==0):
            print("Player choice: L")
          if (totalCounter==1):
            print("Player choice: M")
          if (totalCounter==2):
            print("Player choice: R") 
        return max_val

    else:
        min_val = float('inf') # beta = infinity
        counter=0
        for i, child in enumerate(current_node.children):
            val = alphabeta(child, depth - 1, alpha, beta, True, tracing_enabled)
            min_val = min(min_val, val)
            if (val==min_val):
              totalCounter=counter
            beta = min(beta, val)
            counter=counter+1
            if beta <= alpha:
                if tracing_enabled:
                    print(f'Pruning after processing {child.value}')
                for j, child in enumerate(current_node.children):
                    if j > i:
                        pruned_nodes.append(child)
                break

        current_node.value = min_val
        if tracing_enabled:
            print(f'New value set: {current_node.value}')
            print(str(root))
        if depth==2:
          if (totalCounter==0):
            print("Player choice: L")
          if (totalCounter==1):
            print("Player choice: M")
          if (totalCounter==2):
            print("Player choice: R")
        return min_val


response_tracing = None
while response_tracing != 'y' and response_tracing != 'n':
    response_tracing = input("Do you want to enable step by step tracing? (y/n): ")
response_tracing = response_tracing == 'y'

response_algorithm = None
while response_algorithm != 'minimax' and response_algorithm != 'alphabeta':
 response_algorithm = input("Which algorithm would you like to run? (minimax/alphabeta): ")

values = []
while len(values) != 9:
    value_str = input(f'Input {response_algorithm} values seperated by space: ').strip().split(' ')
    values = [int(val) for val in value_str]

def print_pruned_nodes(pruned_nodes):
    pruned = ' '
    for node in pruned_nodes:
        pruned += node.name + ' '
    print('Pruned Nodes: {}'.format(pruned))

if response_algorithm == 'minimax':
    print('SOLUTION FOR TREE #1')
    test_minimax_1 = [5, 3, 1, 2, 5, 4, 1, 3, 3]
    root = form_tree(test_minimax_1)
    minimax(root, 2, True, response_tracing)
    print()
    print('SOLUTION FOR TREE #2')
    root = form_tree(values)
    minimax(root, 2, True, response_tracing)
elif response_algorithm == 'alphabeta':
    print('SOLUTION FOR TREE #1')
    test_alphabeta_1 = [5, 3, 1, 2, 5, 4, 1, 3, 3]
    root = form_tree(test_alphabeta_1)
    alphabeta(root, 2, float('-inf'), float('inf'), True, response_tracing)
    print_pruned_nodes(pruned_nodes)
    pruned_nodes = []
    print()
    print('SOLUTION FOR TREE #2')
    test_alphabeta_2 = [5, 2, 2, 5, 1, 3, 2, 4, 2]
    root = form_tree(test_alphabeta_2)
    alphabeta(root, 2, float('-inf'), float('inf'), True, response_tracing)
    print_pruned_nodes(pruned_nodes)
    pruned_nodes = []
    print()
    print('SOLUTION FOR TREE #3')
    test_alphabeta_3 = [1, 3, 4, 1, 4, 1, 3, 5, 3]
    root = form_tree(test_alphabeta_3)
    alphabeta(root, 2, float('-inf'), float('inf'), True, response_tracing)
    print_pruned_nodes(pruned_nodes)
    pruned_nodes = []
    print()
    print('SOLUTION FOR TREE #4')
    root = form_tree(values)
    alphabeta(root, 2, float('-inf'), float('inf'), True, response_tracing)
    print_pruned_nodes(pruned_nodes)

