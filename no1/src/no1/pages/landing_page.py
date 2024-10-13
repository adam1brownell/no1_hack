# pages/landing_page.py
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from no1.data.state.global_state import init_global_state
from no1.data.helpers import db_exists


def landing_page(main_window, nav_main):
    # Create a box to hold all elements for the first page
    main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

    # Wrapper function to run initialize_database() and then navigate
    def initialize_and_navigate(widget):
        # Run the initialize_database function
        if not db_exists("global_state"):
            init_global_state()

        # Navigate to the main page
        nav_main(widget)

    # Create a button to navigate to the second page
    button = toga.Button(
        'Welcome to No1',
        on_press=initialize_and_navigate,  # Call the wrapper function
        style=Pack(padding=10)
    )

    # Add button to the box
    main_box.add(button)

    # Set the main window content
    main_window.content = main_box
    return main_box  # Return the box so you can go back to it later
