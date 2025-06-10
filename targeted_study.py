import requests
import json
import argparse

ANKI_CONNECT_URL = "http://localhost:8765"


def find_cards_by_simplified(words):
    """Find card IDs where the 'simplified' field matches any word in the list."""
    card_ids = []

    search_query = "deck:_* " + " OR ".join(f"simplified:{word}" for word in words)

    payload = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": search_query
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    return response['result']

def get_all_cards_in_deck(deck_name):
    """Get all card IDs in a specified deck."""
    request = {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": f"deck:{deck_name}"
        }
    }

    # Send the request to AnkiConnect
    response = requests.post(ANKI_CONNECT_URL, json=request).json()

    # Return the list of card IDs
    return response.get("result", [])

def delete_deck(deck_name):

    request = {
        "action": "deleteDecks",
        "version": 6,
        "params": {
            "decks": [deck_name],
            "cardsToo": True
        }
    }
    # Send the request to AnkiConnect
    response = requests.post(ANKI_CONNECT_URL, json=request).json()

    # Return the list of card IDs
    return response.get("result", [])

def move_cards(deck_name, card_ids):
    add_cards_payload = {
        "action": "changeDeck",
        "version": 6,
        "params": {
            "cards": card_ids,
            "deck": deck_name
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=add_cards_payload).json()
    print(json.dumps(response, indent=2))
def create_filtered_deck(deck_name):
    create_deck_payload = {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    }
    response = requests.post(ANKI_CONNECT_URL, json=create_deck_payload)
    if response.status_code != 200 or response.json().get("error"):
        print(f"Error creating deck {deck_name}: {response.json().get('error')}")
        return

    print(f"Deck '{deck_name}' created successfully.")

def parse_words(words):
    return words.split(',')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create a filtered ANKI deck for targeted study")
    parser.add_argument("-w", "--words", type=str, required=False, help="Words to study")
    parser.add_argument("-d", "--deck", type=str, required=True, help="Target Deck Name")
    parser.add_argument("-r", "--reset", action="store_true", help="Reset Target Deck")
    parser.add_argument("-s", "--source-deck", type=str, required=False, help="Source Deck")


    args = parser.parse_args()
    print(args)
    if args.words is not None:
        words = parse_words(args.words)
        matching_card_ids = find_cards_by_simplified(words)
        create_filtered_deck(args.deck)
        move_cards(args.deck, matching_card_ids)

    if args.reset:
        cards = get_all_cards_in_deck(args.source_deck)
        move_cards(args.deck, cards)
        delete_deck(args.source_deck)