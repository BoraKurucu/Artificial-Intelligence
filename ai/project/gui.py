import time
from tkinter import *
import datetime
first = 0

################################ CROSSWORD GUI CLASS START ################################
class CrosswordGUI:
    """
  A class used to create the CrosswordGUI and keep its attributes.

  Methods
  ---------
  show_root()
    creates the window for GUI.
  draw_canvas()
    Draws the grid of the puzzle using information taken from the website.
  draw_clues()
    Gets the clues from the website then writes them on top of the grid.
  draw_clock(another_puzzle)
    Draws the clock.
  """
    PUZZLE_SIZE = 5
    MARGIN = 10


    def __init__(self, data,solution):
        print("Found the solution")
        print("Constructing user interface...")
        self.solution = solution
        self.data = data
        self.root = Tk()
        self.root.title("The Mini Crossword - NY Times")
        Label(self.root, text='The Mini Crossword', font='Times 48').pack()

        self.draw_canvas(self.data['cells'])
        self.draw_canvas(self.solution)

        #self.draw_canvas2(self.data2)
        self.draw_clues(data)
        self.draw_clock()
        self.show_root()

    def show_root(self):
        self.root.resizable(False, False)
        self.root.mainloop()



    def draw_canvas(self, data):
        """
        Draws the exact square grid in newyork times puzzle using data from newyork times webpage.
        Parameters
        ----------
        data : data taken from newyork times website with selenium.
        """
        canvas = Canvas(self.root, width=520, height=520)
        global first
        if first == 0:
            canvas.pack(fill=BOTH, side=LEFT)
            first = 1
        else:
            canvas.pack(fill=BOTH, side=RIGHT)



        usable = int(canvas['width']) - self.MARGIN * 2

        font_size_number = usable//15
        font_number = ('Arial', font_size_number)
        font_number2 = ('Arial', usable//25)
        font_size_letter = font_size_number * 2
        font_letter = ('Arial', font_size_letter)

        square_width = usable // self.PUZZLE_SIZE

        for i in range(self.PUZZLE_SIZE):
            for j in range(self.PUZZLE_SIZE):
                cell_id = str(i * self.PUZZLE_SIZE + j)
                cell_data = data[cell_id]

                x1 = j * square_width + self.MARGIN
                y1 = i * square_width + self.MARGIN
                x2 = j * square_width + square_width + self.MARGIN
                y2 = i * square_width + square_width + self.MARGIN
                bg = 'black' if cell_data['block'] else 'white'
                canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline='gray', width=1.5)

                x1 = j * square_width + (square_width // 2) + self.MARGIN
                y1 = i * square_width + (2 * square_width // 3) + self.MARGIN - 5
                canvas.create_text(x1, y1, text=cell_data['text'].upper(), font=font_letter)
                x1 = j * square_width + (font_size_number // 2) + self.MARGIN
                y1 = i * square_width + (2 * font_size_number // 3) + self.MARGIN
                canvas.create_text(x1, y1, text=cell_data['number'], font=font_number2)

    def draw_clues(self, data):
        """
        Using selenium gets the clues from the webpage then writes them to the previously created grid.
        Parameters
        ----------
        data : data taken from newyork times website with selenium.
        """
        font_main = 'Arial 12 normal'

        font_title = 'Arial 14 bold'

        pane = PanedWindow()
        pane.pack(fill=X, side=TOP)

        across_pane = PanedWindow(pane)
        across_pane.pack(fill=X, side=LEFT, padx=(self.MARGIN, self.MARGIN), pady=(self.MARGIN, self.MARGIN))
        Label(across_pane, text='ACROSS', font=font_title, anchor='center').pack(fill=BOTH)
        for clue in data['clues']['across']:
            text = clue['id'] + '. ' + clue['text'] + '\n'
            Label(across_pane, text=text, font=font_main, wraplength=500, anchor='w').pack(fill=BOTH)

        down_pane = PanedWindow(pane)
        down_pane.pack(fill=X, side=RIGHT, padx=(self.MARGIN, self.MARGIN), pady=(self.MARGIN, self.MARGIN))
        Label(down_pane, text='DOWN', font=font_title, anchor='center').pack(fill=BOTH)
        for clue in data['clues']['down']:
            text = clue['id'] + '. ' + clue['text'] + '\n'
            Label(down_pane, text=text, font=font_main, wraplength=500, anchor='w').pack(fill=BOTH)

    def draw_clock(self):
        """
        draws the clock and prints the group name with it.
        """
        def update_clock():
            """
            Used to update the clock in regular intervals.
            """
            t = time.strftime("%H:%M:%S")
            clock.configure(text=t)
            self.root.after(1000, update_clock)

        pane = PanedWindow()
        pane.pack(fill=X, side=BOTTOM)
        clock = Label(pane, text='', font='Times 14 italic')
        clock.pack(side=LEFT, pady=(0, self.MARGIN))
        date = Label(pane, text=datetime.date.today().strftime('%A, %B %#d, %Y'), font='Times 14')
        date.pack(side=LEFT, pady=(0, self.MARGIN))
        group_name = Label(pane, text='TERRA', font='Times 14')
        group_name.pack(side=LEFT, pady=(0, self.MARGIN))

        update_clock()


################################ CROSSWORD GUI CLASS END ################################

