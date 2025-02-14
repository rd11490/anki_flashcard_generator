import requests

from create_mp3 import create_mp3
from secrets import chat_gpt_key
from openai import OpenAI
import json
import os
from datetime import datetime
client = OpenAI(api_key=chat_gpt_key)


def make_date_str():
    now = datetime.now()
    return now.strftime("%y-%m-%d-%H:%M:%S")


def create_directory(dir_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, "stories")
    target_dir = os.path.join(base_dir, dir_name)

    try:
        # Create 'cards' folder if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        print(f"Directory created: {target_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
    return target_dir
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
            "query": f"prop:ivl>0"
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

def extract_word(card):
    return card['fields']['Simplified']['value']


def build_paragraph(vocab):
    prompt = f"""
           Using the following vocab list：{', '.join(vocab)}, generate a story in chinese that is at least 250 chinese characters long, has slightly
           complicated sentences and uses normal natural language. Do not include dialog or conversation inside the story.
           Do not include line break characters in the story.
           Provide the following information in JSON format:
           {{
               "story": "", //output story
               "pinyin": "", // Pinyin of the story with tone marks
               "translation": "" // Translation of the story
           }}
            Strictly return only the JSON object, nothing else.
            Strickly write a story that is at least 250 chinese characters long
           """
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant for learning Chinese. Only use words from the given vocabulary list."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,  # Adjust for more creative responses if needed
        max_tokens=10000  # Limit response length
    )
    jsn = json.loads(response.model_dump_json())
    return jsn

cards = get_cards_from_deck('newbie_lazy_cn_deck')
words = []
for card in cards:
    word = extract_word(card)
    words.append(word)

answer = build_paragraph(words)
content = answer['choices'][0]['message']['content']
print(content)
content_jsn = json.loads(content)
story = content_jsn['story']
print(len(story))
byte_length = len(story.encode('utf-8'))
print(byte_length)
date_str = make_date_str()
dir = create_directory(date_str)
create_mp3(story, dir, f'story_{date_str}')
