"""
Group Name: TERRA

Group Members:  Göktuğ Öztürkcan
                Ibrahim Eren Tilla
                Emre Orta
                Mehmet Bora Kurucu
                İsmail Yavuzselim Taşçı

Programming Language: Python 3

In our program, we implemented class precedence list sorter by using the graphs.

"""

single_step=""

def create_fish_hooks(nodes, node):
    if (single_step=="y"):
      print('\nCreating fish hooks....')
    pairs = []
    node_stack = [node]
    while len(node_stack) != 0:
        next_node = node_stack.pop(0)
        parents = nodes[next_node]
        for i, parent in enumerate(parents):
            if i == 0:
                if (single_step=="y"):
                  print('Found new hook: {}--{}'.format(next_node, parent))
                pairs.append((next_node, parent))
            else:
                if (single_step=="y"):
                  print('Found new hook: {}--{}'.format(parents[i - 1], parent))
                pairs.append((parents[i - 1], parent))
            if not parent in node_stack:
                node_stack.append(parent)
    if (single_step=="y"):               
      print('Found new hook: {}--{}'.format(next_node, next_node))
    pairs.append((next_node, next_node))
    return pairs

def wrapper():
    for node in nodes_to_list:
        print('\nSolving for: {}'.format(node))
        class_list = solve(create_fish_hooks(nodes, node))
        print('\nClass precedence list:')
        for element in class_list:
            print(element)

def solve(fish_hooks):
    if (single_step=="y"):
      print('\nSolving....')
    class_list = []
    left_side = []
    right_side = []
    for hook in fish_hooks:
        left_side.append(hook[0])
        right_side.append(hook[1])
    while len(left_side) != 1:
        for element in left_side:
            if not element in right_side:
                element_to_add = element
                break
        if (single_step=="y"):                
          print('Found new class to add to list: {}'.format(element_to_add))
        class_list.append(element_to_add)
        indexes = []
        for i, element in enumerate(left_side):
            if element_to_add == element:
                indexes.append(i)
        count = 0
        for index in indexes:
            print('Deleting hooks: {}--{}'.format(left_side.pop(index - count),right_side.pop(index - count)))
            count += 1
        print()
    if (single_step=="y"):        
      print('Found new class to add to list: {}'.format(left_side[0]))
    class_list.append(left_side[0])
    print('Deleting hooks: {}--{}'.format(left_side.pop(0),right_side.pop(0)))
    return class_list

while (single_step!="y" and single_step!="n"): 
  print("do you want single stepping (y/n)")
  single_step=input()
  if (single_step!="y"or single_step!="n"):
    print("Enter either y or n")
"""
============== PART 1 ==============
=== ifstream, fstream & ofstream ===
"""  
nodes = {}
nodes['ios']      = []
nodes['istream']  = ['ios']
nodes['ostream']  = ['ios']
nodes['iostream'] = ['istream','ostream']
nodes['ifstream'] = ['istream']
nodes['fstream']  = ['iostream']
nodes['ofstream'] = ['ostream']

nodes_to_list = ['ifstream', 'fstream', 'ofstream']

wrapper()

"""
============== PART 2 ==============
CONSULTANT MANAGER, DIRECTOR & PERMANENT MANAGER
"""
nodes = {}
nodes['Employee']           = []
nodes['Temporary Employee'] = ['Employee']
nodes['Manager']            = ['Employee']
nodes['Permanent Employee'] = ['Employee']
nodes['Consultant']         = ['Temporary Employee']
nodes['Consultant Manager'] = ['Consultant', 'Manager']
nodes['Director']           = ['Manager']
nodes['Permanent Manager']  = ['Manager', 'Permanent Employee']

nodes_to_list = ['Consultant Manager', 'Director', 'Permanent Manager']

wrapper()

"""
============== PART 3 ==============
========== CRAZY & JACQUE ============
"""
nodes = {}
nodes['Everything']    = []
nodes['Dwarfs']        = ['Everything']
nodes['Eccentrics']    = ['Dwarfs']
nodes['Teachers']      = ['Dwarfs']
nodes['Programmers']   = ['Dwarfs']
nodes['Athletes']      = ['Dwarfs']
nodes['Endomorphs']    = ['Dwarfs']
nodes['Professors']    = ['Eccentrics', 'Teachers']
nodes['Hackers']       = ['Eccentrics', 'Programmers']
nodes['Weightlifters'] = ['Athletes', 'Endomorphs']
nodes['Shotputters']   = ['Athletes', 'Endomorphs']
nodes['Crazy']         = ['Professors', 'Hackers']
nodes['Jacque']        = ['Weightlifters', 'Shotputters', 'Athletes']

nodes_to_list = ['Crazy', 'Jacque']

wrapper()