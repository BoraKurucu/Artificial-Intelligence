def distance(point1, point2):
  xdif =  abs(point1[0] - point2[0])
  ydif =  abs(point1[1] - point2[1])
  tdif = xdif*xdif + ydif*ydif
  return tdif

class Node:
  def __init__(self, axis, likely_set):
    self.threshold = None
    self.right = None
    self.left = None
    self.likely_set = likely_set
    self.axis = axis
    self.lower_bound = None
    self.upper_bound = None
    self.calculate_threshold()

  def create_next_nodes(self):
    next_axis = 0
    if self.axis == 0:
      next_axis = 1
    self.left = Node(next_axis, self.likely_set[:int(len(self.likely_set) / 2)])
    self.right = Node(next_axis, self.likely_set[int(len(self.likely_set) / 2):])

  def calculate_threshold(self):
    if len(self.likely_set) != 1:
      self.likely_set.sort(key=lambda tup: tup[self.axis])
      self.upper_bound = self.likely_set[int(len(self.likely_set) / 2)]
      self.lower_bound = self.likely_set[int(len(self.likely_set) / 2 - 1)]
      self.threshold = (self.upper_bound[self.axis] + self.lower_bound[self.axis]) / 2
      if verbose:
        comment_axis = 'height'
        if self.axis == 0:
          comment_axis = 'width'
        print('Found a new threshold on {axis} {value}'.format(axis=comment_axis, value=self.threshold))
      self.create_next_nodes()

  def query(self, point):
    if len(self.likely_set) == 1:
      if verbose:
        print('Found a new likely point')
      return self.likely_set[0]
    if point[self.axis] < self.threshold:
      likely_point = self.left.query(point)
      if verbose:
        print('Comparing likely point with the bound')
      if distance(likely_point, point) <= distance(self.upper_bound, point):
        if verbose:
          print('Likely point is better')
        return likely_point
      if verbose:
        print('Bound is better')
      return self.upper_bound
    likely_point = self.right.query(point)
    if verbose:
        print('Comparing likely point with the bound')  
    if distance(likely_point, point) <= distance(self.lower_bound, point):
        if verbose:
          print('Likely point is better')
        return likely_point
    if verbose:
        print('Bound is better')
    return self.lower_bound
    
single_step = ''
while single_step != 'y' and single_step != 'n':
  print('Would you like to enable single stepping (y, n):')
  single_step = input()

verbose = False
if single_step == 'y':
  verbose = True

values = []
while len(values) != 2:
  print('Please enter U(w,h):')
  str_values = input()
  values = str_values.split()
  for i, value in enumerate(values):
    values[i] = int(value)

likely_set = [(1,2, 'red'), (2,6,'red'), (2,5,'orange'), (2,1,'violet'), (4,2,'blue'), (6,1,'green'), (6,5,'purple'), (5,6,'yellow')]

if verbose:
  print("Starting construction of k-d tree...")
root = Node(1, likely_set)

if verbose:
  print('Querying point: {point}'.format(point=[1, 4]))
print('Nearest neighbor found for {values} is: {answer}\n'.format(values=[1, 4], answer=root.query((1, 4)))) #orange
if verbose:
  print('Querying point: {point}'.format(point=[1, 1]))
print('Nearest neighbor found for {values} is: {answer}\n'.format(values=[1, 1], answer=root.query((1, 1)))) #violet
if verbose:
  print('Querying point: {point}'.format(point=[6, 6]))
print('Nearest neighbor found for {values} is: {answer}\n'.format(values=[6, 6], answer=root.query((6, 6)))) #yellow
if verbose:
  print('Querying point: {point}'.format(point=[6, 1]))
print('Nearest neighbor found for {values} is: {answer}\n'.format(values=[6, 1], answer=root.query((6, 1)))) #green
if verbose:
  print('Querying point: {point}'.format(point=values))
print('Nearest neighbor found for {values} is: {answer}\n'.format(values=values, answer=root.query(values))) #This will be the input given by the user