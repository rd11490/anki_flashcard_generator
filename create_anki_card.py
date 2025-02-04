import requests
import base64
"""
HSK Card Model Fields:
Key
Simplified
Pinyin.1
Meaning
Part of speech
Audio
SentenceSimplified
SentencePinyin.1
SentenceMeaning
SentenceAudio
Tags

data:
{
  "word": "李子",
  "pinyin": "lǐzi",
  "definition": "plum",
  "part_of_speech": "noun"
  "example_sentence": "我喜欢吃李子。",
  "example_pinyin": "Wǒ xǐhuān chī lǐzi.",
  "example_translation": "I like to eat plums.",
  "word_audio_path": "PATH_TO_WORD.mp3",
  "sentence_audio_path": "PATH_TO_SENTENCE.mp3"
}
"""
def add_anki_card_with_audio(data, deck_name="newbie_lazy_cn_deck", model_name="HSK"):
    word = data['word']
    pinyin = data['pinyin']
    definition = data['definition']
    sentence = data['example_sentence']
    sentence_pinyin = data['example_pinyin']
    sentence_translation = data['example_translation']
    word_audio_path = data['word_audio_path']
    sentence_audio_path = data['sentence_audio_path']
    part_of_speech = data['part_of_speech']


    # Read and encode the audio file
    with open(word_audio_path, "rb") as audio_file:
        word_audio = base64.b64encode(audio_file.read()).decode('utf-8')

    with open(sentence_audio_path, "rb") as audio_file:
        sentence_audio = base64.b64encode(audio_file.read()).decode('utf-8')


    # Prepare the payload for AnkiConnect
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model_name,
                "fields": {
                    "Key": word,
                    "Simplified": word,
                    "Pinyin.1": pinyin,
                    "Meaning": definition,
                    "Part of speech": part_of_speech,
                    # "Audio": f"[sound:{word}pronunciation.mp3]",  # Reference the audio file here
                    "SentenceSimplified": sentence,
                    "SentencePinyin.1": sentence_pinyin,
                    "SentenceMeaning": sentence_translation,
                    # "SentenceAudio": f"[sound:{word}example.mp3]",  # Reference the audio file here
                },
                "audio": [
                    {
                        "filename": f"{word}pronunciation.mp3",  # The name to be used in Anki
                        "data": word_audio,               # Base64 encoded audio data
                        "fields": ["Audio"]               # Field to link the audio to
                    },{
                        "filename": f"{word}example.mp3",  # The name to be used in Anki
                        "data": sentence_audio,               # Base64 encoded audio data
                        "fields": ["SentenceAudio"]               # Field to link the audio to
                    }
                ],
                "options": {
                    "allowDuplicate": False
                },
                "tags": ["auto-generated"]
            }
        }
    }

    # Send request to AnkiConnect
    response = requests.post("http://localhost:8765", json=payload)
    return response.json()