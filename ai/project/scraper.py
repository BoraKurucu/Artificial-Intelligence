import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumCrosswordHelper:
    """
    A class to determine the web-operations of Selenium.

    Methods
    ---------
    get_clues()
      Returns the data of the clues using the tags that are embedded in the html file.

    get_cells()
      Returns the data of the cells similarly to get_clues().

    reveal_solutions()
      The processes for the revealment of the solutions using Selenium.

    _click_ok()
      Selenium function to click OK button.

    _click_reveal_menu_button()
      Selenium function to click reveal menu button.

    _click_puzzle_reveal_button()
      Selenium function to click reveal button.

    _click_reveal_confirmation_button()
      Selenium function to click confirmation button.

    _close_pop_up()
      Selenium function to close pop-ups.
    """

    def __init__(self):
        options = Options()
        options.headless = False
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        print("Reaching to https://www.nytimes.com/crosswords/game/mini...")
        self.driver.get("https://www.nytimes.com/crosswords/game/mini")
        time.sleep(1)

    def get_clues(self):
        """
        This function first finds the class name tag related with the clues Then,
        it stores the elements which are accessed by the tag names such as 'div','h3','li','span'
        Then the function returns the data array that contains the elements for clues of the puzzle.
        """
        print("Scraping clues...")
        data = {}
        clue_lists = self.driver.find_element_by_class_name('Layout-clueLists--10_Xl')
        divs = clue_lists.find_elements_by_tag_name('div')
        for div in divs:
            title = div.find_element_by_tag_name('h3').text.lower()
            data[title] = []
            list_items = div.find_elements_by_tag_name('li')
            for list_item in list_items:
                spans = list_item.find_elements_by_tag_name('span')
                data[title].append({'id': spans[0].text, 'text': spans[1].text})

        return data

    def get_cells(self):

        """
        Creates an empty set at first, then according to the tags of html, adds cells up to it.
        Returns the set at the end of the function.
        """
        print("Scraping puzzle geometry and solutions...")
        data = {}
        cell_table = self.driver.find_element_by_css_selector('g[data-group=cells]')
        cells = cell_table.find_elements_by_tag_name('g')
        for cell in cells:
            cell_data = {'block': False, 'text': '', 'number': ''}
            rect = cell.find_element_by_tag_name('rect')
            cell_id = rect.get_attribute('id').split('-')[2]
            if 'Cell-block' in rect.get_attribute('class'):
                cell_data['block'] = True
            text_fields = cell.find_elements_by_tag_name('text')
            for text_field in text_fields:
                if text_field.get_attribute('text-anchor') == 'start':
                    cell_data['number'] = text_field.text
                if text_field.get_attribute('text-anchor') == 'middle':
                    cell_data['text'] = text_field.text
            data[cell_id] = cell_data

        return data

    def reveal_solutions(self):
        """
        Using the simple functions below, this function performs the process of revealing solutions.
        """
        print("Revealing the solution...")
        self._click_ok()
        self._click_reveal_menu_button()
        self._click_puzzle_reveal_button()
        self._click_reveal_confirmation_button()
        self._close_pop_up()

    def _click_ok(self):
        """
        Clicks the OK button.
        """
        ok_button = self.driver.find_element_by_css_selector('button[aria-label="OK"]')
        ok_button.click()

    def _click_reveal_menu_button(self):
        """
        Clicks the reveal menu button.
        """
        reveal_button = self.driver.find_element_by_css_selector('button[aria-label="reveal"]')
        reveal_button.click()

    def _click_puzzle_reveal_button(self):
        """
        Clicks the reveal button.
        """
        puzzle_reveal_button = self.driver.find_element_by_link_text('Puzzle')
        puzzle_reveal_button.click()

    def _click_reveal_confirmation_button(self):
        """
        Clicks the confirmation button.
        """
        reveal_button = self.driver.find_element_by_css_selector('button[aria-label="Reveal"]')
        reveal_button.click()

    def _close_pop_up(self):
        """
        Clicks and closes the pop-up screens.
        """
        spans = self.driver.find_elements_by_tag_name('span')
        for span in spans:
            if 'closeX' in span.get_attribute('class'):
                span.click()
                return


class NYCrossword(SeleniumCrosswordHelper):
    """
    A class to initialize and use the Selenium through NYTimes Mini Puzzle

    """

    def __init__(self):
        super(NYCrossword, self).__init__()
        self.reveal_solutions()

    def get_data(self):
        return {'clues': self.get_clues(), 'cells': self.get_cells()}
