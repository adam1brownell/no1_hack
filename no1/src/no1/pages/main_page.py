# # pages/main_page.py
# import toga
# from toga.style import Pack
# from toga.style.pack import COLUMN, CENTER, RIGHT, BOTTOM, ROW
# from .add_data_page import add_data_page

# # Assuming add_data_page is defined elsewhere and handles page navigation

# def main_page(main_window, nav_back):
#     # Create a new box for the main page layout
#     page2_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

#     # Add some content to the main page
#     label = toga.Label('Welcome to No1', style=Pack(padding=10))

#     # Create a container box for the "+" button, aligned to the top-right
#     header_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=10))
    
#     # Create the "+" button
#     add_data_button = toga.Button(
#         "+",
#         on_press=lambda widget: add_data_page(main_window, nav_back), 
#         style=Pack(padding=10)
#     )

#     # Add the "+" button to the header box (top-right corner)
#     header_box.add(add_data_button)

#     # Add the header box (with the "+" button) to the main page box
#     page2_box.add(header_box)
#     page2_box.add(label)

#     # Create a container for the input bar at the bottom
#     input_box = toga.Box(style=Pack(direction=ROW, alignment=BOTTOM, padding=10))

#     # Create TextInput and Submit button
#     user_input = toga.TextInput(placeholder="Respond", style=Pack(flex=1))
#     submit_button = toga.Button('Submit', on_press=lambda widget: on_submit(user_input, page2_box), style=Pack(padding_left=10))

#     # Add the input field and submit button to the input box
#     input_box.add(user_input)
#     input_box.add(submit_button)

#     # Add the input box (bottom) to the main window content
#     main_window.content = page2_box
#     main_window.content.add(input_box)

# def on_submit(user_input, page2_box):
#     # When the user clicks "Submit", the text will render on the page
#     entered_text = user_input.value

#     # Create a new label to display the entered text
#     entered_text_label = toga.Label(f"You entered: {entered_text}", style=Pack(padding=10))

#     # Add the new label to the page
#     page2_box.add(entered_text_label)

#     # Reset the user input box after submitting
#     user_input.value = ""


import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, RIGHT, BOTTOM, ROW
import os
from llama_cpp import Llama
import time

# Importing add_data_page from another file
from .add_data_page import add_data_page

# Load the model on startup
def load_model():
    model = ct.models.MLModel(coreml_model_path)

# Function to stream user and LLM conversation
def stream_conversation_box(box, content, is_user):
    # Create a container for each conversation bubble
    conv_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT if is_user else LEFT, padding=10))

    # Add a label for the text inside the conversation box
    label = toga.Label(content, style=Pack(padding=10, flex=1))
    conv_box.add(label)

    # Add the conversation box to the main content box
    box.add(conv_box)

# Main page layout
def main_page(main_window, nav_back):
    # Create the LLM instance
    llm = load_model()

    # Create the main content box
    page2_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

    # Add a label for the title
    label = toga.Label('Welcome to No1', style=Pack(padding=10))

    # Header with "+" button for navigating to another page
    header_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=10))
    add_data_button = toga.Button(
        "+",
        on_press=lambda widget: add_data_page(main_window, nav_back), 
        style=Pack(padding=10)
    )
    header_box.add(add_data_button)

    # Add header and title to the main box
    page2_box.add(header_box)
    page2_box.add(label)

    # Container for user input at the bottom
    input_box = toga.Box(style=Pack(direction=ROW, alignment=BOTTOM, padding=10))

    # Create TextInput and Submit button
    user_input = toga.TextInput(placeholder="Type your message here...", style=Pack(flex=1))
    submit_button = toga.Button('Submit', on_press=lambda widget: on_submit(user_input, page2_box, llm), style=Pack(padding_left=10))

    # Add input field and submit button to input box
    input_box.add(user_input)
    input_box.add(submit_button)

    # Add input box to the main window content
    main_window.content = page2_box
    main_window.content.add(input_box)

# Submit user input and get LLM response
def on_submit(user_input, page2_box, llm):
    # Get user input text
    entered_text = user_input.value

    # Display the user's input
    stream_conversation_box(page2_box, f'User: {entered_text}', is_user=True)

    # Generate response from LLM
    if llm:
        llm_response = llm(entered_text)  # Generate response from LLM
        stream_conversation_box(page2_box, f'LLM: {llm_response["choices"][0]["text"]}', is_user=False)

    # Reset the user input box after submitting
    user_input.value = ""
