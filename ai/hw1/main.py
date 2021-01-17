"""
Group Name: TERRA

Group Members:  Göktuğ Öztürkcan
                Ibrahim Eren Tilla
                Emre Orta
                Mehmet Bora Kurucu
                İsmail Yavuzselim Taşçı

Programming Language: Python 3

"""

"""
====================== HOW TO RUN THE CODE ======================
-Make sure you have python installed in your environment.
-Paste the following command into your terminal: python main.py
"""

class Action:
    """
    A class used to control the actions of missionaries and cannibals
    according to the position of the boat
    
    Methods 
    --------
    is_action_possible(state)
        Returns true if missionaries and cannibals on either end is greater 
        or equal to the missionaries and cannibals on the boat.
    
    generate_possible_state(state)
        Generates the possible actions on both ends and updates the current 
        state with new state.
    """
    def __init__(self, missionaries_on_boat, cannibals_on_boat):
        """
        Parameters
        ----------
        missionaries_on_boat : int
            The number of missionaries on the boat
        cannibals_on_boat : int 
            The number of cannibals on the boat
        """
        self.missionaries_on_boat = missionaries_on_boat
        self.cannibals_on_boat = cannibals_on_boat
    
    def is_action_possible(self, state):
        """
        Ensures that missionaries on left and right side is not less than the 
        missionaries and cannibals on boat. Since the program creates new 
        states by adding or subtracting the missionaries & cannibals on both
        ends from missionaries & cannibals on boat, this function avoids the
        impossible states where the number of people remaining in left and right side 
        is negative.
        Parameters
        ----------
        state : TYPE
            state object
        """
        if state.boat_position == 0:
            return (self.missionaries_on_boat <= state.missionaries_on_left) and (self.cannibals_on_boat <= state.cannibals_on_left)
        if state.boat_position == 1:
            return (self.missionaries_on_boat <= state.missionaries_on_right) and (self.cannibals_on_boat <= state.cannibals_on_right)

    def generate_possible_state(self, state):
        """
        First,it checks whether the action is possible. Then, if the boat is on 
        left side, cannibals and missionaries get in the boat and are carried to
        right. If the boat is on right side, the exact oppsite is applied. This 
        sequential process creates the new state.
        updated.
        
        Parameters
        ----------
        state : TYPE
            state object.
        """
        if not self.is_action_possible(state):
              return None

        if state.boat_position == 0: # initially boat is on left side
              cannibals_on_left = state.cannibals_on_left - self.cannibals_on_boat # cannibals get in the boat
              missionaries_on_left = state.missionaries_on_left - self.missionaries_on_boat # missionaries get in the boat

              cannibals_on_right = state.cannibals_on_right + self.cannibals_on_boat 
              missionaries_on_right = state.missionaries_on_right + self.missionaries_on_boat
              boat_position = 1 # boat is on right side

        if state.boat_position == 1:
              cannibals_on_left = state.cannibals_on_left + self.cannibals_on_boat
              missionaries_on_left = state.missionaries_on_left + self.missionaries_on_boat

              cannibals_on_right = state.cannibals_on_right - self.cannibals_on_boat
              missionaries_on_right = state.missionaries_on_right - self.missionaries_on_boat
              boat_position = 0 # boat is on left side
        
        # state is updated according to the new positions
        new_state = State(cannibals_on_left, missionaries_on_left, boat_position, cannibals_on_right, missionaries_on_right)

        if new_state.is_possible():
              return new_state

        return None


class State:
    def __init__(self, cannibal, missionaries, boat, cannibals_right, missionaries_right):
        """
        Parameters
        ----------
        cannibal : int
            The number of cannibals on left side
        missionaries : int
            The number of missionaries on left side
        boat : int
            The position of the boat 
        cannibals_right : int
            The number of cannibals on right side
        missionaries_right : int
            The number of missionaries on right side
        """
        self.boat_position = boat
        self.cannibals_on_left = cannibal
        self.missionaries_on_left = missionaries
        self.cannibals_on_right = cannibals_right
        self.missionaries_on_right = missionaries_right

    def is_possible(self):
        """
        Avoids impossible states        
        Returns
        -------
        bool
            returns false if cannibals are greater than missionaries on either left
            or right sides
        """
        if self.cannibals_on_left > self.missionaries_on_left and not self.missionaries_on_left == 0  or self.cannibals_on_right > self.missionaries_on_right and not self.missionaries_on_right == 0:
            return False
        return True

    def is_equal(self, state):
        """
        Checks if given state is equal to this state  
        Returns
        -------
        bool
            returns false if given state is not equal to this state or true if it is equal
        """
        return (self.boat_position == state.boat_position) and (self.cannibals_on_left == state.cannibals_on_left) and (self.missionaries_on_left == state.missionaries_on_left)

class Node:
    """
    A class used to generate the node with specified state, depth and action
    """
    def __init__(self, state, predecessor, depth, action):
        """
        Parameters
        ----------
        state : TYPE
            state object
        predecessor : TYPE
            represents the prior state than the current state
        depth : int
            the number of edges from the node to the root node
        action : TYPE
            represents the transition betweeen states
        """
        self.state = state
        self.predecessor = predecessor
        self.depth = depth
        self.action = action
    
    def is_state_unique(self):
        """
        Avoids reversible actions by checking whether the current state is the 
        same as predecessor
        Returns
        -------
        bool
            False if predecessor state is equal to the current
        """
        pre = self.predecessor
        while pre:
            if pre.state.is_equal(self.state):
                  return False
            pre = pre.predecessor
        return True
    
    def print_solution(self):
        """
        The following method prints the solution in the according manner
        """
        result = ''
        if not self.predecessor:
            for i in range(self.state.cannibals_on_left):
                result += 'C'
            result += '\n'
            for i in range(self.state.missionaries_on_left):
                result += 'M'
            result += '\n'
            print(result)
            return
        
        self.predecessor.print_solution()
        status = 'SEND' 
        if self.state.boat_position == 0:
            status = 'RETURN'
        result = '{0: <7} {1: <1} CANNIBALS {2: <1} MISSIONARIES'.format(status, self.action.cannibals_on_boat, self.action.missionaries_on_boat)
        result += '\n'

        for i in range(self.state.cannibals_on_left):
            result += 'C'

        result += '{0: <22}'.format('')
        for i in range(self.state.cannibals_on_right):
            result += 'C'

        result += '\n'
        for i in range(self.state.missionaries_on_left):
            result += 'M'

        
        result += '{0: <22}'.format('')
        for i in range(self.state.missionaries_on_right):
            result += 'M'
            
        result += '\n'
        print(result)

def create_actions(cannibal, missionaries, boat_capacity):
    """
    Parameters
    ----------
    cannibal : int
        The total number of cannibals
    missionaries : int
        The total number of missionaries
    boat_capacity : int
        The number of people that the boat can carry
    Returns
    -------
    possible_actions : list
        It holds the possible actions from initial to the goal state
    """
    possible_actions = []
    missionaries_on_boat = 1 # beginning of an action 
    cannibals_on_boat = 0
    while missionaries_on_boat <= boat_capacity and missionaries_on_boat <= missionaries:
        while cannibals_on_boat <= missionaries_on_boat and cannibals_on_boat <= boat_capacity - missionaries_on_boat :
            possible_actions.append(Action(missionaries_on_boat, cannibals_on_boat)) # an action is added to the list
            cannibals_on_boat += 1 # cannibals get in the boat until it exceeds missionaries and the boat capacity
        cannibals_on_boat = 0 # cannibals on boat are released 
        missionaries_on_boat += 1 # missionaries get in the boat until it exceeds the boat capacity
    cannibals_on_boat = 1
    missionaries_on_boat = 0 
    while cannibals_on_boat <= boat_capacity and  cannibals_on_boat <= cannibal:
        possible_actions.append(Action(missionaries_on_boat, cannibals_on_boat))
        cannibals_on_boat += 1
    possible_actions.append(Action(0, 1)) 
    return possible_actions


def solve(cannibal, missionaries, boat_capacity):
    """
    In our program, we have the root(initial) and goal nodes. We use DFS
    to find a path that delivers the root node to the goal node. First, we create 
    possible actions and store them in a list. Then, we iteratively check the actions 
    in the list and create the new states. If the state is possible, a new node 
    with n+1 (where n is the depth) away from the initial node is created. If the 
    node has not been visited yet, we add the node into the list of path. Then, we assign 
    the current node to the the last node that is added to the list by returning it 
    from the path. Finally, we check whether this node is the goal node. If so, 
    the current node is added to the list of goal nodes to make it ready for printing.
    Our program generates solution for the case where there are 5 missionaries,
    5 cannibals and the boat capacity is 3. In addition to that, we have choosen the 2b question and our program also generate solution for this case where there are 6 missionaries, 6 cannibals and the boat capacity is 5.        
    
    Parameters
    ----------
    cannibal : int
        The total number of cannibals
    missionaries : int
        The total number of missionaries
    boat_capacity : int
        The number of people that the boat can carry

    """
    initial_state = State(cannibal, missionaries, 0, 0, 0) # e.g.,5M,5C and boat is on left
    initial_node = Node(initial_state, None, 1, None) 

    goal_state = State(0, 0, 1, cannibal, missionaries) # e.g.,5M,5C and boat is on right

    path = [initial_node] # holds the path between starting node and the destination 

    possible_actions = create_actions(cannibal, missionaries, boat_capacity)
    
    while not len(path) == 0:
        """
        In order to make the program work as a BFS rather than DFS,
        following line of code can be arranged like this:
        current_node = path.pop(0) 
        """
        current_node = path.pop() # current node is the last node added to the path

        if current_node.state.is_equal(goal_state): 
            goal_node = current_node
            break
      
        for action in possible_actions:
            new_state = action.generate_possible_state(current_node.state)
            if new_state: # checks whether the state is an impossible state or not
                new_node = Node(new_state, current_node, current_node.depth + 1, action)
                if new_node.is_state_unique(): # checks whether the state is unique
                      path.append(new_node) # add the node to the list

    goal_node.print_solution()

"""
We designed our program to provide solutions for both (6,6,4) and (6,6,5)
"""
value = 0
while value != '3':
    print("Please enter 1 to solve puzzle with 5C, 5M AND 3 BOAT SIZE")
    print("Please enter 2 to solve puzzle with 6C, 6M AND 5 BOAT SIZE")
    value = input("Please enter 3 to exit:\n")
    print('\n')
    if value == '1':
        solve(5,5,3)
    elif value == '2':
        solve(6,6,5)
        




"""
====================== OUTPUT FOR 5C 5M 3 BOAT SIZE ======================
CCCCC
MMMMM

SEND    3 CANNIBALS 0 MISSIONARIES
CC                      CCC
MMMMM                      

RETURN  1 CANNIBALS 0 MISSIONARIES
CCC                      CC
MMMMM                      

SEND    3 CANNIBALS 0 MISSIONARIES
                      CCCCC
MMMMM                      

RETURN  2 CANNIBALS 0 MISSIONARIES
CC                      CCC
MMMMM                      

SEND    0 CANNIBALS 3 MISSIONARIES
CC                      CCC
MM                      MMM

RETURN  1 CANNIBALS 1 MISSIONARIES
CCC                      CC
MMM                      MM

SEND    0 CANNIBALS 3 MISSIONARIES
CCC                      CC
                      MMMMM

RETURN  1 CANNIBALS 0 MISSIONARIES
CCCC                      C
                      MMMMM

SEND    3 CANNIBALS 0 MISSIONARIES
C                      CCCC
                      MMMMM

RETURN  1 CANNIBALS 0 MISSIONARIES
CC                      CCC
                      MMMMM

SEND    2 CANNIBALS 0 MISSIONARIES
                      CCCCC
                      MMMMM


====================== OUTPUT FOR 6C 6M 5 BOAT SIZE ======================
CCCCCC
MMMMMM

SEND    5 CANNIBALS 0 MISSIONARIES
C                      CCCCC
MMMMMM                      

RETURN  1 CANNIBALS 0 MISSIONARIES
CC                      CCCC
MMMMMM                      

SEND    2 CANNIBALS 0 MISSIONARIES
                      CCCCCC
MMMMMM                      

RETURN  1 CANNIBALS 0 MISSIONARIES
C                      CCCCC
MMMMMM                      

SEND    0 CANNIBALS 5 MISSIONARIES
C                      CCCCC
M                      MMMMM

RETURN  2 CANNIBALS 2 MISSIONARIES
CCC                      CCC
MMM                      MMM

SEND    2 CANNIBALS 3 MISSIONARIES
C                      CCCCC
                      MMMMMM

RETURN  1 CANNIBALS 0 MISSIONARIES
CC                      CCCC
                      MMMMMM

SEND    2 CANNIBALS 0 MISSIONARIES
                      CCCCCC
                      MMMMMM
"""