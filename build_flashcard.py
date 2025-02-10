import os
import sys

from create_anki_card import add_anki_card_with_audio
from create_example_sentence import generate_chinese_sentence
from create_mp3 import create_mp3
import json

def create_card_directory(word):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, "cards")
    target_dir = os.path.join(base_dir, word)

    try:
        # Create 'cards' folder if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        print(f"Directory created: {target_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
    return target_dir

def save_json(data, directory):
    with open(f"{directory}/data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def build_flash_card(word):
    target_dir = create_card_directory(word)
    sentence_data = generate_chinese_sentence(word)
    sentence = sentence_data['example_sentence']
    word_file_path = create_mp3(word, target_dir, f'WORD_{word}')
    sentence_file_path = create_mp3(sentence, target_dir, f'SENTENCE_{word}')
    sentence_data['word_audio_path'] = word_file_path
    sentence_data['sentence_audio_path'] = sentence_file_path
    save_json(sentence_data, target_dir)
    add_anki_card_with_audio(sentence_data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_card_dir.py <word>")
        sys.exit(1)

    word = sys.argv[1]
    build_flash_card(word)