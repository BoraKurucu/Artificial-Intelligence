import requests
import math

"""
    Static Functions
    ---------
    query()
      This function queries Datamus API for the given parameters.
      We can query using means-like, left-context, right-context, topic and known until now.

    prune()
      This function reevaluates results coming from the Datamuse API. We check the length of the
      results with our puzzle and also we add score fields when we do not get that field from API.

    make_request()
      This function either sends a request as 'meanslike' 'left-context' 'right-context' depending
      on the structure of the clue.

    get_difference()
      This function is used to calculate the scores of candidate words.
      Divides the scores with the scores to their right and returns the division array.

    def create_puzzle_from_existing():
      This function simply creates a deepcopy of the given puzzle and returns it.
      
    Global Variables
    ----------
    url: Base url of the Datamuse API. Used in query() function.

    iter: Iteration number that we are currently in.
"""

url = 'https://api.datamuse.com/words'
iter = 0



def query(sp, ml=None, lc=None, rc=None, topic=None):
  if sp.find('?') != -1:
    if ml:
      if ml.find(',') != -1:
        ml = ml[:ml.find(',')]

    payload = {'ml': ml, 'sp': sp, 'max': 2, 'lc': lc, 'rc': rc, 'topics': topic}

    r = requests.get(url, params=payload)
    print('Requesting {}'.format(r.url))

    results = r.json()

    results = prune(results, sp)
    if len(results) != 0:
      return results
  else:
    payload = {'sp': sp, 'max': 1}
    r = requests.get(url, params=payload)
    print('Requesting {}'.format(r.url))
    results = r.json()

    results = prune(results, sp)
    return results

def prune(results, sp):
  for result in results:
    if not 'score' in result.keys():
      result['score'] = 1
    result['word'] = result['word'].replace(" ", "")

  results = [result for result in results if len(result['word']) == len(sp)]

  return results
  
def make_request(known, clue):
  rc = None
  lc = None
  topic = None
  ml = None

  position = clue.find('(')
  if position != -1:
    p2 = clue.find(')')
    topic = clue[position + 1:p2]
    clue = clue[:position] + clue[p2 + 1:]

  position = clue.find('___')
  if position != -1:
    if position == 0:
      rc = clue[4:]
      indexes = [rc.find('.'), rc.find(','), rc.find(' ')]
      indexes = [x for x in indexes if x != -1]
      if len(indexes) != 0:
        rc = rc[:min(indexes)]
    else:
      lc = clue[:position - 1]
      indexes = [lc.find('.'), lc.find(','), lc.find(' ')]
      indexes = [x for x in indexes if x != -1]
      if len(indexes) != 0:
        lc = lc[max(indexes):]
  else:
    ml = clue

  return query(known, ml, lc, rc, topic)

def get_difference(arr):
  for i in range(len(arr) - 1):
    if arr[i + 1] == 1:
      break
    if 'score' in arr[i].keys() and 'score' in arr[i + 1].keys():
      arr[i]['score'] = arr[i]['score'] / arr[i + 1]['score']

def create_puzzle_from_existing(puzzle_to_copy):
  puzzle = []

  for row in puzzle_to_copy:
    puzzle.append([])
    for node in row:
      new_node = Node(node.text, node.block, node.clue_across, node.clue_down, node.across_candidates, node.down_candidates, node.across_solved, node.down_solved, node.number)
      puzzle[-1].append(new_node)
  return puzzle

class Node:
  """
    A class to represent individual puzzle cells

    Methods
    ---------
    to_string()
      This is the methos we used while printing the puzzle at each iteration. 
      Basically prints the necessary information of the Node class.

    Variables
    ----------
    text: The character that is in a tile of the puzzle

    block: Keeps if tile is writable or blocked

    clue_across: Keeps the number of across clue starting from the tile, if it exists

    clue_down: Keeps the number of down clues starting from the tile, if it exists

    across_candidates: Candidate words for the across clue starting from the tile

    down_candidates: Candidate words for the downwards clue starting from the tile

    across_solved: Solved word going across that is starting from the current tile

    down_solved: Solved word going down that is starting from the current tile

    number: Clue number of the node
      
  """
  def __init__(self, text, block, clue_across, clue_down, across_candidates, down_candidates, across_solved, down_solved, number):
    self.clue_across = clue_across
    self.clue_down = clue_down
    self.text = text
    self.block = block
    self.across_candidates = across_candidates
    self.down_candidates = down_candidates
    self.across_solved = across_solved
    self.down_solved = down_solved
    self.number = number
  
  def to_string(self):
    if self.text == '':
      return ' '
    return self.text
  

class PuzzleTree:
  """
    A class to represent candidate puzzles in a tree-like manner.

    Methods
    ---------
    solve()
      Recursive function to solve our puzzle. It makes use of query() and get_difference() functions.
      Basically it creates a new PuzzleTree for each and every candidate puzzle. Then it deepens the search
      starts from the most promising puzzle.
  
    Variables
    ---------
    puzzle: Array to keep the current puzzle
    
    parent: Parent of the current Puzzle
      
  """
  def __init__(self, puzzle, parent, score):
    self.PUZZLE_LENGTH = 5
    self.parent = parent
    self.puzzle = puzzle
    self.children = []
    self.score = score
  
  def solve(self):
    global iter
    iter += 1
    print('\n\n---------------------------------\n\n')
    print('Iteration {}'.format(iter))
    print('\nPuzzle:\n')
    for row in self.puzzle:
      text = ""
      for element in row:
        text= text + element.to_string()
      print(text)

    print('\nRequests:\n')
    for i, row in enumerate(self.puzzle):
      for j, element in enumerate(row):
        if element.clue_across:
          known = ''
          for k in range(j, self.PUZZLE_LENGTH):
            if row[k].block:
              break
            if row[k].text == '':
              known = known + '?'
            else:
              known = known + row[k].text
          if not element.across_solved:
            element.across_candidates = make_request(known, element.clue_across)
            if element.across_candidates == None:
              element.across_candidates = []
            get_difference(element.across_candidates)
        if element.clue_down:
          known = ''
          for k in range(i, self.PUZZLE_LENGTH):
            if self.puzzle[k][j].block:
              break
            if self.puzzle[k][j].text == '':
              known = known + '?'
            else:
              known = known + self.puzzle[k][j].text
          if not element.down_solved:
            element.down_candidates = make_request(known, element.clue_down)
            if element.down_candidates == None:
              element.down_candidates = []
            get_difference(element.down_candidates)

    candidates = []
    solved = 0
    for i, row in enumerate(self.puzzle):
      for j, element in enumerate(row):
        if element.across_solved:
          solved += 1
        elif element.clue_across and len(element.across_candidates) != 0:
          candidates.append(element.across_candidates[0])
        if element.down_solved:
          solved += 1
        elif element.clue_down and len(element.down_candidates) != 0:
          candidates.append(element.down_candidates[0])

    if len(candidates) == 0:
      if solved == self.PUZZLE_LENGTH * 2:
        return self
      return None
 
    candidates = sorted(candidates, key=lambda tup: tup['score'], reverse=True)

    print('\nCandidate Words:\n')
    for candidate in candidates:
      print(candidate)
      new_puzzle = create_puzzle_from_existing(self.puzzle)
      for i, row in enumerate(new_puzzle):
        for j, element in enumerate(row):
          if element.across_candidates and candidate == element.across_candidates[0]:
            for k, text in enumerate(candidate['word']):
                row[k + j].text = text
            element.across_solved = True
            break
          if element.down_candidates and candidate == element.down_candidates[0]:
            for k, text in enumerate(candidate['word']):
                new_puzzle[k + i][j].text = text
            element.down_solved = True
            break
      new_tree = PuzzleTree(new_puzzle, self, self.score + candidate['score'])
      self.children.append(new_tree)

    if len(self.children) == 0:
      return None
    for child in self.children:
      result = child.solve()
      if result != None:
        return result

class Solver:
  """
    Base wrapper class for solving the puzzle. It makes use of PuzzleTree and provides a simple
    interface to outside world.

    Methods
    ---------
    create_puzzle()
      This method is the initial point for our solver. Basically it creates an empty puzzle
      from scraped data to use as a root node in the PuzzleTree.

    create_format()
      This method creates a JSON formatted version of the solution. This format is same as the
      scraped data format. Having a single format for both initial puzzle and solution is very
      convenient when we render both in gui.py

  """
  def __init__(self):
    self.PUZZLE_LENGTH = 5
  
  def create_puzzle(self, clues, layout):
    puzzle = []
    for i in range(self.PUZZLE_LENGTH):
      puzzle.append([])
    
    for key in layout.keys():
      text = ''
      block = layout[key]['block']
      clue_across = None
      clue_down = None
      number = layout[key]['number']
      if number != '':
        for clue in clues['across']:
          if number == clue['id']:
            clue_across = clue['text']
        for clue in clues['down']:
          if number == clue['id']:
            clue_down = clue['text']
      node = Node(text, block, clue_across, clue_down, [], [], False, False, number)
      puzzle[int(math.floor(int(key) / self.PUZZLE_LENGTH))].append(node)
    tree = PuzzleTree(puzzle, None, 0)

    return self.create_format(tree.solve())
  
  def create_format(self, tree):
    puzzle = tree.puzzle

    result = {}

    for i, row in enumerate(puzzle):
      for j, element in enumerate(row):
        sub = {}
        sub['block'] = element.block
        sub['text'] = element.text.upper()
        sub['number'] = element.number
        result['{}'.format(i * self.PUZZLE_LENGTH + j)] = sub
    return result

"""
---------------------------OLD PUZZLE DATA FOR OUR USE-----------------------------------

#clues = {'across': [{'id': '1', 'text': 'House members, for short'}, {'id': '5', 'text': "Yo-Yo Ma's instrument"}, {'id': '6', 'text': 'Identity-concealing name'}, {'id': '7', 'text': 'Food that New Haven and New York are noted for'}, {'id': '8', 'text': 'March Madness org.'}], 'down': [{'id': '1', 'text': 'Historical artifact'}, {'id': '2', 'text': 'Phillipa Soo\'s role in "Hamilton"'}, {'id': '3', 'text': '___ Hotel, iconic building overlooking Central Park'}, {'id': '4', 'text': 'Sammy with 609 career home runs'}, {'id': '5', 'text': '___ Crunch (cereal)'}]}
#layout = {'0': {'block': True, 'text': '', 'number': ''}, '1': {'block': False, 'text': 'R', 'number': '1'}, '2': {'block': False, 'text': 'E', 'number': '2'}, '3': {'block': False, 'text': 'P', 'number': '3'}, '4': {'block': False, 'text': 'S', 'number': '4'}, '5': {'block': False, 'text': 'C', 'number': '5'}, '6': {'block': False, 'text': 'E', 'number': ''}, '7': {'block': False, 'text': 'L', 'number': ''}, '8': {'block': False, 'text': 'L', 'number': ''}, '9': {'block': False, 'text': 'O', 'number': ''}, '10': {'block': False, 'text': 'A', 'number': '6'}, '11': {'block': False, 'text': 'L', 'number': ''}, '12': {'block': False, 'text': 'I', 'number': ''}, '13': {'block': False, 'text': 'A', 'number': ''}, '14': {'block': False, 'text': 'S', 'number': ''}, '15': {'block': False, 'text': 'P', 'number': '7'}, '16': {'block': False, 'text': 'I', 'number': ''}, '17': {'block': False, 'text': 'Z', 'number': ''}, '18': {'block': False, 'text': 'Z', 'number': ''}, '19': {'block': False, 'text': 'A', 'number': ''}, '20': {'block': False, 'text': 'N', 'number': '8'}, '21': {'block': False, 'text': 'C', 'number': ''}, '22': {'block': False, 'text': 'A', 'number': ''}, '23': {'block': False, 'text': 'A', 'number': ''}, '24': {'block': True, 'text': '', 'number': ''}}


#layout = {'0': {'block': False, 'text': 'A', 'number': '1'}, '1': {'block': False, 'text': 'B', 'number': '2'}, '2': {'block': False, 'text': 'I', 'number': '3'}, '3': {'block': False, 'text': 'T', 'number': '4'}, '4': {'block': True, 'text': '', 'number': ''}, '5': {'block': False, 'text': 'S', 'number': '5'}, '6': {'block': False, 'text': 'O', 'number': ''}, '7': {'block': False, 'text': 'D', 'number': ''}, '8': {'block': False, 'text': 'A', 'number': ''}, '9': {'block': True, 'text': '', 'number': ''}, '10': {'block': False, 'text': 'H', 'number': '6'}, '11': {'block': False, 'text': 'I', 'number': ''}, '12': {'block': False, 'text': 'A', 'number': ''}, '13': {'block': False, 'text': 'L', 'number': ''}, '14': {'block': False, 'text': 'L', 'number': '7'}, '15': {'block': True, 'text': '', 'number': ''}, '16': {'block': False, 'text': 'S', 'number': '8'}, '17': {'block': False, 'text': 'H', 'number': ''}, '18': {'block': False, 'text': 'O', 'number': ''}, '19': {'block': False, 'text': 'O', 'number': ''}, '20': {'block': True, 'text': '', 'number': ''}, '21': {'block': False, 'text': 'E', 'number': '9'}, '22': {'block': False, 'text': 'O', 'number': ''}, '23': {'block': False, 'text': 'N', 'number': ''}, '24': {'block': False, 'text': 'S', 'number': ''}}
#clues = {'across': [{'id': '1', 'text': 'The slightest amount'}, {'id': '5', 'text': 'Vodka ___ (popular two-ingredient cocktail)'}, {'id': '6', 'text': 'Start of a group email'}, {'id': '8', 'text': '"Go away, fly!"'}, {'id': '9', 'text': 'Billions and billions of years'}], 'down': [{'id': '1', 'text': 'Fire proof?'}, {'id': '2', 'text': 'With 3-Down, U.S. capital + state with the fewest number of combined letters'}, {'id': '3', 'text': 'See 2-Down'}, {'id': '4', 'text': "Hawk's claw"}, {'id': '7', 'text': 'Part of U.C.L.A.'}]}


#layout = {'0': {'block': True, 'text': '', 'number': ''}, '1': {'block': True, 'text': '', 'number': ''}, '2': {'block': False, 'text': 'T', 'number': '1'}, '3': {'block': False, 'text': 'A', 'number': '2'}, '4': {'block': False, 'text': 'B', 'number': '3'}, '5': {'block': False, 'text': 'S', 'number': '4'}, '6': {'block': False, 'text': 'M', 'number': '5'}, '7': {'block': False, 'text': 'I', 'number': ''}, '8': {'block': False, 'text': 'L', 'number': ''}, '9': {'block': False, 'text': 'E', 'number': ''}, '10': {'block': False, 'text': 'K', 'number': '6'}, '11': {'block': False, 'text': 'A', 'number': ''}, '12': {'block': False, 'text': 'P', 'number': ''}, '13': {'block': False, 'text': 'P', 'number': ''}, '14': {'block': False, 'text': 'A', 'number': ''}, '15': {'block': False, 'text': 'I', 'number': '7'}, '16': {'block': False, 'text': 'T', 'number': ''}, '17': {'block': False, 'text': 'S', 'number': ''}, '18': {'block': False, 'text': 'O', 'number': ''}, '19': {'block': False, 'text': 'N', 'number': ''}, '20': {'block': False, 'text': 'S', 'number': '8'}, '21': {'block': False, 'text': 'H', 'number': ''}, '22': {'block': False, 'text': 'Y', 'number': ''}, '23': {'block': True, 'text': '', 'number': ''}, '24': {'block': True, 'text': '', 'number': ''}}
#clues = {'across': [{'id': '1', 'text': 'Running total at a bar'}, {'id': '4', 'text': "Photographer's request"}, {'id': '6', 'text': 'Greek "K"'}, {'id': '7', 'text': '"Oh, you wanna go? Let\'s go!"'}, {'id': '8', 'text': 'Bashful'}], 'down': [{'id': '1', 'text': 'A little drunk'}, {'id': '2', 'text': 'Purina dog food brand'}, {'id': '3', 'text': 'Word after jelly or coffee'}, {'id': '4', 'text': 'Sports equipment with which you can do a "pizza stop"'}, {'id': '5', 'text': 'Class that has its pluses and minuses'}]}


#layout ={'0': {'block': False, 'text': 'D', 'number': '1'}, '1': {'block': False, 'text': 'O', 'number': '2'}, '2': {'block': False, 'text': 'F', 'number': '3'}, '3': {'block': False, 'text': 'F', 'number': '4'}, '4': {'block': False, 'text': 'S', 'number': '5'}, '5': {'block': False, 'text': 'A', 'number': '6'}, '6': {'block': False, 'text': 'P', 'number': ''}, '7': {'block': False, 'text': 'R', 'number': ''}, '8': {'block': False, 'text': 'I', 'number': ''}, '9': {'block': False, 'text': 'L', 'number': ''}, '10': {'block': False, 'text': 'N', 'number': '7'}, '11': {'block': False, 'text': 'E', 'number': ''}, '12': {'block': False, 'text': 'E', 'number': ''}, '13': {'block': False, 'text': 'R', 'number': ''}, '14': {'block': False, 'text': 'A', 'number': ''}, '15': {'block': False, 'text': 'C', 'number': '8'}, '16': {'block': False, 'text': 'R', 'number': ''}, '17': {'block': False, 'text': 'E', 'number': ''}, '18': {'block': False, 'text': 'S', 'number': ''}, '19': {'block': False, 'text': 'S', 'number': ''}, '20': {'block': False, 'text': 'E', 'number': '9'}, '21': {'block': False, 'text': 'A', 'number': ''}, '22': {'block': False, 'text': 'R', 'number': ''}, '23': {'block': False, 'text': 'T', 'number': ''}, '24': {'block': False, 'text': 'H', 'number': ''}}
#clues={'across': [{'id': '1', 'text': 'Removes politely, as a hat'}, {'id': '6', 'text': 'Rainy month'}, {'id': '7', 'text': "___ Tanden, Biden's pick to lead the O.M.B."}, {'id': '8', 'text': 'Salad green with a peppery taste'}, {'id': '9', 'text': 'Subject of the famous photo "The Blue Marble"'}], 'down': [{'id': '1', 'text': 'See 4-Down'}, {'id': '2', 'text': 'Lincoln Center performance'}, {'id': '3', 'text': 'Less restricted'}, {'id': '4', 'text': 'With 1-Down, tradition for the married couple at a wedding reception'}, {'id': '5', 'text': 'Symbol that shares a key with "?"'}]}


#layout = {'0': {'block': True, 'text': '', 'number': ''}, '1': {'block': False, 'text': 'C', 'number': '1'}, '2': {'block': False, 'text': 'L', 'number': '2'}, '3': {'block': False, 'text': 'U', 'number': '3'}, '4': {'block': False, 'text': 'B', 'number': '4'}, '5': {'block': True, 'text': '', 'number': ''}, '6': {'block': False, 'text': 'L', 'number': '5'}, '7': {'block': False, 'text': 'A', 'number': ''}, '8': {'block': False, 'text': 'N', 'number': ''}, '9': {'block': False, 'text': 'E', 'number': ''}, '10': {'block': False, 'text': 'M', 'number': '6'}, '11': {'block': False, 'text': 'A', 'number': ''}, '12': {'block': False, 'text': 'Y', 'number': ''}, '13': {'block': False, 'text': 'B', 'number': ''}, '14': {'block': False, 'text': 'E', 'number': ''}, '15': {'block': False, 'text': 'O', 'number': '7'}, '16': {'block': False, 'text': 'R', 'number': ''}, '17': {'block': False, 'text': 'E', 'number': ''}, '18': {'block': False, 'text': 'O', 'number': ''}, '19': {'block': True, 'text': '', 'number': ''}, '20': {'block': False, 'text': 'M', 'number': '8'}, '21': {'block': False, 'text': 'A', 'number': ''}, '22': {'block': False, 'text': 'R', 'number': ''}, '23': {'block': False, 'text': 'X', 'number': ''}, '24': {'block': True, 'text': '', 'number': ''}}
#clues = {'across': [{'id': '1', 'text': 'What a black three-leaf clover represents'}, {'id': '5', 'text': 'Highway division'}, {'id': '6', 'text': 'Wishy-washy R.S.V.P.'}, {'id': '7', 'text': "Snack that's the most-used brand name in New York Times crosswords"}, {'id': '8', 'text': '"The Communist Manifesto" co-author'}], 'down': [{'id': '1', 'text': '___ Barton, nurse who founded the Red Cross'}, {'id': '2', 'text': 'Crust, mantle or core'}, {'id': '3', 'text': 'Remove from the packaging'}, {'id': '4', 'text': 'Creature with five eyes and six legs'}, {'id': '6', 'text': 'CBS sitcom starring Allison Janney and Anna Faris'}]}
"""