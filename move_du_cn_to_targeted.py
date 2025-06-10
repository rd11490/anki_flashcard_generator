import requests
import csv

from targeted_study import find_cards_by_simplified, move_cards


# Function to extract Chinese characters from a file
def extract_chinese(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        words = []
        for row in reader:
            words.append(row['# Exported from Du Chinese'])
        return words

def get_cards_from_deck(deck_name):
    """
    Retrieves all cards from a specified Anki deck and their contents.

    :param deck_name: Name of the Anki deck.
    :return: List of dictionaries containing card details.
    """
    # AnkiConnect API URL
    anki_connect_url = "http://localhost:8765"

    # Step 1: Find all card IDs in the specified deck
    find_cards_payload = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": f"deck:{deck_name}"
        }
    }
    response = requests.post(anki_connect_url, json=find_cards_payload)
    card_ids = response.json().get("result", [])
    if not card_ids:
        print(f"No cards found in deck: {deck_name}")
        return []

    # Step 2: Get detailed information for each card
    cards_info_payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {
            "cards": card_ids
        }
    }
    response = requests.post(anki_connect_url, json=cards_info_payload)
    cards_info = response.json().get("result", [])

    return cards_info

# Example usage
if __name__ == "__main__":
    file_path = 'du_cn_word_list/DuChinese_2025-06-06_1749185170.csv'
    deck_name = "targeted_study"  # Replace with your deck name
    word_list = extract_chinese(file_path)
    cards = get_cards_from_deck('newbie_lazy_cn_deck')
    card_list = []
    cards_to_create = []
    cards_to_move = []
    for card in cards:
        word = card['fields']['Simplified']['value']
        card_list.append(word)

    for word in word_list:
        if word not in card_list:
            cards_to_create.append(word)
        elif word in card_list:
            cards_to_move.append(word)

    # print(len(cards_to_create))
    for word in cards_to_move:
        print(word)
        try:
            matching_card_ids = find_cards_by_simplified(word)
            move_cards('targeted_study', matching_card_ids)
        except:
            print('Could not create card')




