import sqlite3
import os
import json
import httpx  # Replaced requests with httpx
import pandas as pd
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from datetime import datetime
from no1.data.helpers import db_exists, get_db_path

DB_PATH = get_db_path('oura_data')

def prompt_for_api_key(main_window):
    # Create a small window to ask for API key input
    input_window = toga.Window(title="Enter API Key")

    # Create a text input for the API key
    api_key_input = toga.TextInput(placeholder="Enter your Oura API Key", style=Pack(padding=10, width=200))

    # Define a function to handle the button press
    def on_submit(widget):
        api_key = api_key_input.value
        if api_key:  # Ensure the user entered something
            pull_oura_data(api_key)  # Call pull_oura_data with the entered key
            input_window.close()  # Close the input window
        else:
            toga.MessageBox.info(main_window, "Error", "Please enter a valid API key.")  # Show an error

    # Create a button to submit the API key
    submit_button = toga.Button("Submit", on_press=on_submit, style=Pack(padding=10))

    # Create a box to hold the input and button
    input_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))
    input_box.add(api_key_input)
    input_box.add(submit_button)

    # Set the content of the input window and show it
    input_window.content = input_box
    input_window.show()

def pull_oura_data(access_token, start_date='1970-01-01', end_date=None, endpoint='all'):
    """
    Pull Oura Ring Data using httpx
    """
    
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    daily_endpoints = [
        "daily_activity",
        "daily_readiness",
        "daily_resilience",
        "daily_sleep",
        "daily_spo2",
        "daily_stress",
        "sleep",
        "sleep_time",
    ]

    # Check endpoint values
    if isinstance(endpoint, str):
        if endpoint == 'all':
            endpoints = daily_endpoints
        else:
            endpoints = [endpoint]
    elif isinstance(endpoint, list):
        endpoints = endpoint
    else:
        raise Exception("Endpoint needs to be str or list")
    
    params = {
        'start_date': start_date,  
        'end_date': end_date      
    }

    # Initialize the DataFrame
    oura_pd = None

    with httpx.Client() as client:  # Using httpx instead of requests
        for e in endpoints:
            print(f"Fetching data for {e}")
            url = f'https://api.ouraring.com/v2/usercollection/{e}'
            response = client.get(url, headers=headers, params=params)

            if response.status_code == 200:
                payload = response.json()

                for entry in payload['data']:
                    flat_entry = pd.json_normalize(entry).dropna(axis=1, how='all')

                    if oura_pd is None:
                        oura_pd = flat_entry
                        continue

                    day = entry['day']
                    if oura_pd['day'].isin([day]).any():
                        oura_pd.loc[oura_pd['day'] == day, flat_entry.columns] = flat_entry.values
                    else:
                        oura_pd = pd.concat([oura_pd, flat_entry], ignore_index=True)
            else:
                print(f'Error: {response.status_code}, Message: {response.text}')

    # Convert the list columns to JSON strings before saving to the database
    def convert_lists_to_json(df):
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():  # Check if column contains lists
                df[col] = df[col].apply(json.dumps)  # Convert lists to JSON strings
        return df

    # Convert list columns to JSON
    if oura_pd is not None:
        oura_pd = convert_lists_to_json(oura_pd)

        # Save the DataFrame to SQLite
        conn = sqlite3.connect(DB_PATH)
        oura_pd.to_sql('oura_data', conn, if_exists='append', index=False)
        conn.commit()
        conn.close()

    return True
