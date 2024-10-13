# app.py

"""
Self-Improvement through Data & Conversation

cd build && rm -rf no1 && cd .. && briefcase build iOS && briefcase run iOS
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER

from no1.pages.main_page import main_page  # Import the main_page
from no1.pages.landing_page import landing_page  # Import the landing_page
from no1.pages.add_data_page import add_data_page  # Import the landing_page

class HelloWorldApp(toga.App):

    def startup(self):
        # Set the main window
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Load the landing page (first page)
        self.main_box = landing_page(self.main_window, self.nav_main)

        # Show the main window
        self.main_window.show()

    def nav_main(self, widget):
        # Load the main page
        main_page(self.main_window, self.nav_back)

    def nav_back(self, widget):
        # Return to the first page (landing page)
        self.main_window.content = self.main_box

def main():
    return HelloWorldApp()

if __name__ == '__main__':
    main().main_loop()
