import os
import json

from create_anki_card import add_anki_card_with_audio


def file_exists(file_path):
    return os.path.exists(file_path)


import requests

ANKI_CONNECT_URL = "http://localhost:8765"


def check_card_exists(word):
    """Check if a card with the given ID exists."""
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'deck:_* Key:{word}'
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    result = response.get("result")
    return result[0] if len(result) > 0 else None  # Returns True if the card exists


def delete_card(card_id):
    """Delete a card by ID if it exists."""
    payload = {
        "action": "deleteNotes",
        "version": 6,
        "params": {
            "notes": [card_id]
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    print(f"Deleted card {card_id}: {response}")


def fix_all_cards():
    folder_path = "cards"  # Change this to your folder path

    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

    for folder in subfolders:
        fix_path(folder)


def fix_path(folder):
    # Path to the JSON file
    file_path = f"{folder}/data.json"

    if (file_exists(file_path)):
        # Open and read the file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Parses JSON into a Python dictionary

        word = data['word']
        print(word)
        card_id = check_card_exists(word)
        if card_id is not None:
            delete_card(card_id)
        add_anki_card_with_audio(data)


fix_all_cards()