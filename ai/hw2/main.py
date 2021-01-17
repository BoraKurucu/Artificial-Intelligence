"""
Group Name: TERRA

Group Members:  Göktuğ Öztürkcan
                Ibrahim Eren Tilla
                Emre Orta
                Mehmet Bora Kurucu
                İsmail Yavuzselim Taşçı

Programming Language: Python 3

In our program, we used the heuristic number 1 which is the number of misplaced tiles.
It is an admissible heuristics since it provides us to calculate the total path length by 
the summation of the distance already travelled and the number of misplaced tiles. The duplicate tiles do not pose a problem since we eliminate the duplicate tiles while solving the puzzle.


Disclaimer: We provided a GUI at the end, although it works for
the most part, for some states it does not work because it runs out of space.
"""

"""
====================== HOW TO RUN THE CODE ======================
-Make sure you have python installed in your environment.
-Paste the following command into your terminal: python main.py
"""

import random
import copy
import matplotlib.pyplot as plt
from operator import attrgetter

goal = [[1,2,3,4], [2,3,4,5], [3,4,5,5], [4,5,5,[]]]

################################ PUZZLE CLASS START ################################

class Puzzle:
  """
  A class used to create the puzzle and keep it's attributes.

  Methods
  ---------
  get_random_place()
    Gets a random place according to the position of blank space then swaps the position of blank space.
  shuffle()
    Calls get random place 10 times to shuffle the Puzzle.
  is_equal()
    Returns true if the puzzle is in goal state, false otherwise.
  is_equal2(another_puzzle)
    Returns true if another_puzzle is equal to the objects puzzle. False otherwise.   
  to_string()
    Prints the 2D puzzle of the object.
  number_of_misplaced_tiles()
    Returns the number of misplaced tiles according to manhattan distance.  
  generate_possible_next_puzzle()
    gets all the next possible puzzles and returns them in an array.
  create_next_array(move)
    According to the move given creates the next array that will come up.
  get_possible_moves()  
    Return all the possible directions up, down, left, right as boolean.
  get_point()
    Return number of moves + number of misplaced tiles.
  """
  def __init__(self, initial_array, move_number, old_puzzle, blank, cost):
    """
    Parameters
    ----------
    initial_array : int[][]
      The initial array.
    move_number : int 
      Total number of moves for the puzzle
    old puzzle: int[][] 
      The old puzzle array
    blank : (int,int) 
      Location of the blank space 
    cost : int 
      Cost used to get the puzzle   
    """
    self.puzzle_array = initial_array
    self.move_number = move_number
    self.old_puzzle = old_puzzle
    self.blank = blank
    self.cost = cost + self.get_point()

  
  def get_random_place(self):
    """
    First it sets all possible directions to 1. Then, if the blank space is on a point where it can't go in of the directions that direction is set to 0. Then to randomize the integers for the directions are multiplied with a random number between 0 and 100. The biggest number is chosen as the direction to go. Then the blank space is swapped with the direction. 
    """    
    (i,j) = self.blank
    up = 1
    down = 1
    left = 1
    right = 1
    
    if i == 0:
      up = 0
    if i == 3:
      down = 0
    if j == 0:
      left = 0
    if j == 3:
      right = 0
    
    up    *= random.randint(1,100)
    down  *= random.randint(1,100)
    left  *= random.randint(1,100)
    right *= random.randint(1,100)
    
    maximum = max(up,down,left,right)
    if maximum == up and up != 0:
      i += -1
    elif maximum == down and down != 0:
      i += 1 
    elif maximum == right and right != 0:
      j += 1
    elif maximum == left and left != 0:
      j += -1

    (element1,element2) = (i,j)
    oldx, oldy = self.blank
    self.puzzle_array[oldx][oldy] = self.puzzle_array[element1][element2]
    self.puzzle_array[element1][element2] = []
    self.blank = (element1, element2)
    
  def shuffle(self):
    """
    Calls get_random_place 10 times to shuffle the puzzle.
    """   
    for i in range(10):
        self.get_random_place()
    
  def is_equal(self):
    """
    Checks if the Puzzle is equal to the goal. If so returns True, otherwise false. 
    """   
    return goal == self.puzzle_array
    
  def is_equal2(self, another_puzzle):
    """
    Compares the puzzle_array of the puzzle with another puzzles puzzle_array. If they are equal returns true. Otherwise false. 
    Parameters
        ----------
        another_puzzle : Puzzle object
          puzzle_array of the another_puzzle object is used for comparison.

          
    """   
    return another_puzzle.puzzle_array == self.puzzle_array

  def to_string(self):
    """
    Prints out the puzzle_array of the Puzzle. Along with blank tile's location, total number of moves and cost.
    """ 
    for i in self.puzzle_array:
      print(i)
    print("current blank is " + str(self.blank) + "\ntotal number of moves is " + str(self.move_number) + "\ncurrent missing tiles is " + (str)(self.number_of_misplaced_tiles()) + "\nso cost is " + str(self.cost))
    print("")
  def to_string2(self):
    for r in self.puzzle_array:
      print(r)

  def number_of_misplaced_tiles(self):
    """
    Calculate the number of misplaced tiles by comparing the differences in the current puzzle_array and the goal array.
    """ 
    number_of_misplaced_tiles = 0
    for i in range(4):
        for j in range(4):
            if self.puzzle_array[i][j] != goal[i][j]:
                number_of_misplaced_tiles += 1
    return number_of_misplaced_tiles

  def generate_possible_next_puzzle(self):
    """
    Method that generates possible next puzzle which will be used in the solve class
    where it will determine the possible ways of the blank tile to move in order to
    solve the puzzle.

    Returns
    -------
    nexts : array 
      returns the array list that contains the next puzzles
    """      
    nexts = []
    (up, down, left, right) = self.get_possible_moves()
    if up:
      (i,j) = self.blank;
      i = i - 1
      new_blank = (i,j)
      nexts.append(Puzzle(self.create_next_array(0), self.move_number + 1, self,new_blank,self.cost))
    if down:
      (i,j) = self.blank;
      i = i + 1
      new_blank = (i,j)
      nexts.append(Puzzle(self.create_next_array(1), self.move_number + 1, self,new_blank,self.cost))
    if left:
      (i,j) = self.blank;
      j = j - 1
      new_blank = (i,j)
      nexts.append(Puzzle(self.create_next_array(2), self.move_number + 1, self,new_blank,self.cost))
    if right:
      (i,j) = self.blank;
      j = j + 1
      new_blank = (i,j)
      nexts.append(Puzzle(self.create_next_array(3), self.move_number + 1, self,new_blank,self.cost))


    return nexts
  
  def create_next_array(self, move):
    """
    Creates the next possible array according to the given move number
    
    Parameters
    ----------
    move : int
      integer value that determines in which direction the next possible array will go in.

    Returns
    -------
    new_array : array
      returns the newly created array after deepcopying and changing the values accordingly.
    """
    (i,j) = self.blank
    element1 = i
    element2 = j
    if move == 0:
      element1 = i - 1
    elif move == 1:  
      element1 = i + 1
    elif move == 2:  
      element2 = j - 1
    elif move == 3:
      element2 = j + 1
    new_array = copy.deepcopy(self.puzzle_array)
    oldx, oldy = self.blank
    new_array[oldx][oldy] = new_array[element1][element2]
    new_array[element1][element2] = []
    return new_array


  def get_possible_moves(self):
    """
    A function which returns the moves that are possible according to the 
    variables i and j that holds the position of the blank (-1 numerically) 
    Returns
    -------
    up : int
      represents the upward move
    down : int
      represents the downward move
    left : int
      represents the move towards left
    right : int
      represents the move towards right
    """
  
    (i,j) = self.blank # position of the blank
    up = True
    down = True
    left = True
    right = True
      
    if i == 0:
      up = False
    if i == 3:
      down = False
    if j == 0:
      left = False
    if j == 3:
      right = False
    return (up, down, left, right) # returns possible moves 
    
  def get_point(self):
    """
    returns the sum of the number of moves and the number of misplaced tiles. The number 
    of moves corresponds to the distance travelled in A* algorithm. f(N) = g(N) + h(N) where g(N) is the already travelled( number of moves) until N. 
    """
    return self.move_number + self.number_of_misplaced_tiles()

################################ PUZZLE CLASS END ################################


################################ SOLVE CLASS START ################################

class Solver:
  """
  The class that takes a puzzle and solves it by backtracking the blank tile's movements

  Methods
  ---------
  backtrace(parent, start, end)
    An auxiliary function that backtraces the given puzzle blank space tile's movements through the parent puzzle. 
    Returns the path which the tile came to its current state.

  solve()
    Solves the given puzzle by using backtracking until the puzzle reached the goal state.
    
  """


  def __init__(self, puzzle_obj):
    """
    Constructor method that initializes the Solve object

    Parameters
    ----------
    puzzle_obj : Puzzle object
      The puzzle that was given for the Solve class to solve.
    """
    self.puzzle_obj = puzzle_obj 

  def backtrace(self, parent, start, end):
    """
    This method takes the given list and reverses it back to where it started.

    Parameters
    ----------
    parent : Puzzle list
        List that contains parent puzzles.
    start  : Puzzle object
        Starting puzzle.
    end    : Puzzle object
        Ending puzzle.
        
    Returns
    -------
    path : list
        returns the backtracked puzzles in a list
    """
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path    
      
  def solve(self):
    """
    This method solves the given puzzle. It initializes an empty list and a queue at first. 
    Then, updates the resulting array by backtracking the given Puzzle and prints the puzzle in each step of the solving process.
    """
    parent = {}
    maximum_number_of_paths = 0
    q = []
    q.append(self.puzzle_obj)
    front = q[0]
    start = q[0]
    result = []
    while(len(q) > 0 and front.is_equal() == False):
        maximum_number_of_paths = max(len(q), maximum_number_of_paths)
        front = q.pop()
        if front.is_equal() == True:
            result = self.backtrace(parent,start,front)
            
        #front.to_string()
        nexts = front.generate_possible_next_puzzle()
        is_seen = False
        for i in nexts:
            for el in q:
                if i.is_equal2(el):
                    is_seen = True
                    break
            for el in q:
                if i.is_equal2(parent[el]):
                    is_seen = True
                    break
            if is_seen:
                is_seen = False
                continue             
            parent[i] = front
            q.append(i)
            
        q.sort(key = attrgetter('cost'), reverse = True)
    
    return (result, maximum_number_of_paths)


################################ SOLVE CLASS END ################################



################################ MAIN START ################################

""" 
MAIN: The following code is where we use both the Puzzle and Solve class in order 
to create and solve 12 distinct puzzles.
"""  
list = []

while len(list) < 12:
  p1 = Puzzle(copy.deepcopy(goal), 0, None,(3,3),0)
  p1.shuffle()
  is_same = False
  for obj in list:
    if obj.is_equal2(p1):
      is_same = True
  if is_same == False:
    list.append(p1)

print("==================== INITIAL STATES ====================")

count = 1
for i in list:
  print("Initial State for S{}".format(count))
  i.to_string2()
  print("")
  count += 1

# x axis values 
x_axis = ["S3","S4","S5","S6","S7","S8","S9","S10","S11","S12"]


print("\nNOW, HERE ARE THE TWO GRAPHICAL SOLUTIONS FOR S1 AND S2\n")


print_count = 0
y_axis = []

for i in list:
  solver = Solver(i)
  (result, queue_size) = solver.solve()
  if print_count < 2:
    print_count += 1
    for i in range(len(result)):
      result[i].to_string()
    if result:
      print("==================== PUZZLE HAS BEEN SOLVED ====================")
      print("\n")
  else:
    y_axis.append(queue_size)

"""
Plot
"""
# plotting the points  
plt.scatter(x_axis, y_axis) 
plt.show() 

################################ MAIN END ################################


################################ OUTPUT ################################

"""
==================== INITIAL STATES ====================
Initial State for S1
[1, 2, 3, 4]
[2, 3, 5, []]
[3, 4, 4, 5]
[4, 5, 5, 5]

Initial State for S2
[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, [], 5, 5]

Initial State for S3
[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, 5, 5, []]

Initial State for S4
[1, 2, 4, 4]
[2, 3, 3, []]
[3, 4, 5, 5]
[4, 5, 5, 5]

Initial State for S5
[1, 2, [], 4]
[2, 3, 3, 5]
[3, 5, 4, 5]
[4, 4, 5, 5]

Initial State for S6
[[], 2, 3, 4]
[1, 2, 4, 5]
[3, 3, 5, 5]
[4, 4, 5, 5]

Initial State for S7
[1, 2, 3, 4]
[2, 3, 4, []]
[3, 4, 5, 5]
[4, 5, 5, 5]

Initial State for S8
[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, [], 5]
[4, 5, 5, 5]

Initial State for S9
[1, 2, 3, 4]
[2, 3, 4, 5]
[[], 3, 4, 5]
[4, 5, 5, 5]

Initial State for S10
[1, 2, 5, 3]
[2, [], 3, 4]
[3, 4, 4, 5]
[4, 5, 5, 5]

Initial State for S11
[1, 2, 3, 4]
[2, 3, 5, 5]
[3, 5, 4, 4]
[4, [], 5, 5]

Initial State for S12
[1, 2, 3, 4]
[2, 3, 4, 5]
[[], 3, 5, 5]
[4, 4, 5, 5]


NOW, HERE ARE THE TWO GRAPHICAL SOLUTIONS FOR S1 AND S2

[1, 2, 3, 4]
[2, 3, 5, []]
[3, 4, 4, 5]
[4, 5, 5, 5]
current blank is (1, 3)
total number of moves is 0
current missing tiles is 4
so cost is 0

[1, 2, 3, 4]
[2, 3, [], 5]
[3, 4, 4, 5]
[4, 5, 5, 5]
current blank is (1, 2)
total number of moves is 1
current missing tiles is 3
so cost is 4

[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, [], 5]
[4, 5, 5, 5]
current blank is (2, 2)
total number of moves is 2
current missing tiles is 2
so cost is 8

[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, []]
[4, 5, 5, 5]
current blank is (2, 3)
total number of moves is 3
current missing tiles is 2
so cost is 13

[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, 5, 5, []]
current blank is (3, 3)
total number of moves is 4
current missing tiles is 0
so cost is 17

==================== PUZZLE HAS BEEN SOLVED ====================


[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, [], 5, 5]
current blank is (3, 1)
total number of moves is 0
current missing tiles is 2
so cost is 0

[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, 5, [], 5]
current blank is (3, 2)
total number of moves is 1
current missing tiles is 2
so cost is 3

[1, 2, 3, 4]
[2, 3, 4, 5]
[3, 4, 5, 5]
[4, 5, 5, []]
current blank is (3, 3)
total number of moves is 2
current missing tiles is 0
so cost is 5

==================== PUZZLE HAS BEEN SOLVED ====================
"""
