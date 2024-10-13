# pages/add_data_page.py
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, RIGHT, BOTTOM, ROW
from no1.data.state.global_state import is_saved, save_state, get_state
import no1.data.api.oura as oura

DATA_SOURCES = {
    "Oura": {
        "name": "Oura",
        "is_connected": False,
        "image_ref": "assets/oura-logo.jpg"
    },
    "Apple Healthkit": {
        "name": "Apple Healthkit",
        "is_connected": False,
        "image_ref": "assets/apple-logo.jpg"
    },
    "Whoop": {
        "name": "Whoop",
        "is_connected": False,
        "image_ref": "assets/whoop-logo.jpg"
    },
    "Garmin": {
        "name": "Garmin",
        "is_connected": False,
        "image_ref": "assets/garmin-logo.jpg"
    },
}


def add_data_page(main_window, go_back):
    # Create the add data page box
    add_data_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20))

    def open_overlay(source):
        # Create a box to hold the entire overlay content
        overlay_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20))

        # Create a box to hold the "X" button, aligned to the top-right
        close_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT))

        # Add an "X" button to close the overlay
        close_button = toga.Button(
            "X",
            on_press=lambda widget: add_data_page(main_window, go_back),  # Go back to the main add_data_page
            style=Pack(padding=10)
        )

        # Add the close button to the close_box (aligned to the right)
        close_box.add(close_button)

        # Label showing the selected data source
        button_str = 'Disconnect from' if source['is_connected'] else 'Connect to'
        source_label = toga.Label(f"{button_str} {source['name']}", style=Pack(padding=10))

        # Button to "connect" and close the overlay
        connect_button = toga.Button(
            "Connect",
            on_press=lambda widget: connect_source(main_window, source),
            style=Pack(padding=10)
        )
        disconnect_button = toga.Button(
            "Disconnect",
            on_press=lambda widget: disconnect_source(source),
            style=Pack(padding=10)
        )

        # Add the close box (with the "X" button) to the overlay
        overlay_box.add(close_box)

        # Add the label and connect button to the overlay
        overlay_box.add(source_label)
        if source['is_connected']:
            overlay_box.add(disconnect_button)
        else:
            overlay_box.add(connect_button)

        # Show the overlay
        main_window.content = overlay_box

    def connect_source(main_window, source):
        if source['name'] == "Oura":
            oura.prompt_for_api_key(main_window)
        else:
            print("Other")
        source['is_connected'] = True
        add_data_page(main_window, go_back)  # Close the overlay by going back to the add data page

    def disconnect_source(source):
        source['is_connected'] = False
        add_data_page(main_window, go_back)  # Close the overlay by going back to the add data page

    # Loop through data sources and create buttons to open their overlays
    for source in DATA_SOURCES.values():
        
        bcolor = 'green' if source['is_connected'] else 'grey'
        fcolor = 'white' if source['is_connected'] else 'black'
        button_str = 'Disconnect' if source['is_connected'] else 'Connect'

        label = toga.Label(source['name'], style=Pack(padding=10, color=fcolor))

        row_box = toga.Box(style=Pack(
            direction=ROW,
            padding=10,
            background_color=bcolor,  # Border color
        ))

        # Load the image from resources
        image = toga.Image(f"{source['image_ref']}")
        image_view = toga.ImageView(image, style=Pack(padding=10, width=50, height=50))

        # Create a button for each data source to open its overlay
        connect_button = toga.Button(
            button_str,
            on_press=lambda widget, s=source: open_overlay(s),  # Pass the current source to the lambda
            style=Pack(padding=10)
        )

        row_box.add(label)
        row_box.add(image_view)
        row_box.add(connect_button)

        add_data_box.add(row_box)

    # Add a back button to go back to the main page
    back_button = toga.Button(
        "Back",
        on_press=go_back,
        style=Pack(padding=10)
    )
    add_data_box.add(back_button)

    # Set the content of the main window to the add data page
    main_window.content = add_data_box
