# pages/main_page.py
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, RIGHT, BOTTOM, ROW
from .add_data_page import add_data_page

# Assuming add_data_page is defined elsewhere and handles page navigation

def main_page(main_window, nav_back):
    # Create a new box for the main page layout
    page2_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

    # Add some content to the main page
    label = toga.Label('Welcome to Page 2!', style=Pack(padding=10))

    # Create a container box for the "+" button, aligned to the top-right
    header_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=10))
    
    # Create the "+" button
    add_data_button = toga.Button(
        "+",
        on_press=lambda widget: add_data_page(main_window, nav_back),  # Assuming add_data_page is correctly defined
        style=Pack(padding=10)
    )

    # Add the "+" button to the header box (top-right corner)
    header_box.add(add_data_button)

    # Add the header box (with the "+" button) to the main page box
    page2_box.add(header_box)
    page2_box.add(label)

    # Create a container for the input bar at the bottom
    input_box = toga.Box(style=Pack(direction=ROW, alignment=BOTTOM, padding=10))

    # Create TextInput and Submit button
    user_input = toga.TextInput(placeholder="Enter your text here", style=Pack(flex=1))
    submit_button = toga.Button('Submit', on_press=lambda widget: on_submit(user_input, page2_box), style=Pack(padding_left=10))

    # Add the input field and submit button to the input box
    input_box.add(user_input)
    input_box.add(submit_button)

    # Add the input box (bottom) to the main window content
    main_window.content = page2_box
    main_window.content.add(input_box)

def on_submit(user_input, page2_box):
    # When the user clicks "Submit", the text will render on the page
    entered_text = user_input.value

    # Create a new label to display the entered text
    entered_text_label = toga.Label(f"You entered: {entered_text}", style=Pack(padding=10))

    # Add the new label to the page
    page2_box.add(entered_text_label)

    # Reset the user input box after submitting
    user_input.value = ""
