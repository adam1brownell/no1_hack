import sqlite3
import os
import json
import requests
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

def initialize_oura_db():
    # Ensure the db folder exists
    if not db_exists("oura_data"):
        print(DB_PATH)
        print("***")
        print(get_db_path('oura_data'))
        print("***")
        # os.makedirs(os.path.dirname(get_db_path('oura_data')))

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table to store Oura data (adjust columns as needed)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS oura_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            activity_score INTEGER,
            readiness_score INTEGER,
            sleep_score INTEGER,
            spo2_score INTEGER,
            stress_score INTEGER,
            -- Add more fields as per your API data structure
            UNIQUE(day)  -- Ensure no duplicate entries for the same day
        )
    ''')

    conn.commit()
    conn.close()

def pull_oura_data(access_token, start_date='1970-01-01',end_date=None, endpoint='all'):
    """
    Pull Oura Ring Data
    """

    if end_date == None:
        end_date = datetime.today().strftime('%Y-%d-%m')
        
    headers = {
    'Authorization': f'Bearer {access_token}',
    }
    
    daily_endpoints =[
        "daily_activity",
        "daily_readiness",
        "daily_resilience",
        "daily_sleep",
        "daily_spo2",
        "daily_stress",
        "sleep",
        "sleep_time",
    ] 

    # check endpoint values
    if type(endpoint) == str:
        if endpoint == 'all':
            endpoints = daily_endpoints
        else:
            endpoints = list(endpoint)
    elif type(endpoint) != list:
        raise Exception("Endpoint needs to be str or list")
    else:
        endpoints = endpoint
        
    for e in endpoints:
        if e not in daily_endpoints:
            raise Exception(f"Unknown Endpoint '{endpoint}'")
    
    params = {
        'start_date': start_date,  
        'end_date': end_date      
    }

    # data_dict = dict()
    oura_pd = None
    oura_sleep_pd = None

    for e in endpoints:
        print(e)
        endpoint = f'https://api.ouraring.com/v2/usercollection/{e}'
        response = requests.get(endpoint, headers=headers, params=params)
        # Check the response
        if response.status_code == 200:
            payload = response.json()

            for entry in payload['data']:
                flat_entry = pd.json_normalize(entry).dropna(axis=1, how='all')
                # for col in flat_entry.columns:
                #     print(col,": ",flat_entry[col])
                # break
                
                if oura_pd is None:
                    oura_pd = flat_entry
                    continue
                day = entry['day']

                if e == 'sleep':
                    continue
                    # if oura_sleep_pd is None:
                    #     oura_sleep_pd = flat_entry
                    #     continue
                    # else:
                    #     oura_sleep_pd = pd.concat([oura_sleep_pd,flat_entry], ignore_index=True)

                if oura_pd['day'].isin([day]).any():
                    oura_pd.loc[oura_pd['day'] == day, flat_entry.columns] = flat_entry.values
                else:
                    oura_pd = pd.concat([oura_pd,flat_entry], ignore_index=True)
        else:
            print(f'Error: {response.status_code}, Message: {response.text}')

    # Convert the list columns to JSON strings
    def convert_lists_to_json(df):
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():  # Check if column contains lists
                df[col] = df[col].apply(json.dumps)  # Convert lists to JSON strings
        return df

    # Convert list columns to JSON
    oura_pd = convert_lists_to_json(oura_pd)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    oura_pd.to_sql(DB_PATH, conn, if_exists='append', index=False)

    return True