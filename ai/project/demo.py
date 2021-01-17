"""
Group Name: TERRA

Group Members:  Göktuğ Öztürkcan
                Ibrahim Eren Tilla
                Emre Orta
                Mehmet Bora Kurucu
                İsmail Yavuzselim Taşçı

Programming Language: Python 3

In this demo, we are retrieving the crossword puzzle data from the nytimes website. Then,
we are processing said data into smaller smaller chunks where we transform it to a line-by-line
data. We put the data in our GUI, where the user can see the puzzle clearly. For the answers, we
are using Selenium for the "reveal solutions" use-case. After revealing the data, we take it and
put in the the GUI of the puzzle as well.
"""

"""
====================== HOW TO RUN THE CODE ======================
-Make sure you have python installed in your environment.
-You need to install selenium with following command: pip install selenium
-You need to to have appropriate chromedriver in the same location as this file. To download appropriate driver please check out: https://chromedriver.chromium.org/
-Use the following command into your terminal to run the program: python demo.py
"""

from gui import CrosswordGUI
from scraper import NYCrossword
from solver import Solver

data = NYCrossword().get_data()
print(data["cells"])
print(data["clues"])
s = Solver()
solution = s.create_puzzle(data['clues'], data['cells'])
gui = CrosswordGUI(data=data, solution=solution)
