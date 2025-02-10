import re
import requests

from build_flashcard import build_flash_card


# Function to extract Chinese characters from a file
def extract_chinese(file_path):
    chinese_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Ignore blank lines
                # Extract only Chinese characters
                chinese_chars = re.findall(r'[\u4e00-\u9fff]+', line)
                if chinese_chars:
                    chinese_list.extend(chinese_chars)
    return chinese_list

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
file_path = 'common_words/common_chinese_words'
deck_name = "newbie_lazy_cn_deck"  # Replace with your deck name
word_list = extract_chinese(file_path)
cards = get_cards_from_deck(deck_name)
card_list = []
cards_to_create = []
for card in cards:
    word = card['fields']['Simplified']['value']
    card_list.append(word)

for word in word_list:
    if word not in card_list:
        cards_to_create.append(word)

# print(len(cards_to_create))
for word in cards_to_create:
    print(word)
    try:
        build_flash_card(word)
    except:
        print('Could not create card')




