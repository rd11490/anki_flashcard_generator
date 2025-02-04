# anki_flashcard_generator
Auto generates anki flashcards using chatgpt and google cloud tts

##### NOTE:
This project is currently not generalized to match multiple languages, decks, etc. It was built for my specific use case


#### To Run
```commandline
python build_flashcard.py 李子
```

#### Process:
1. Calls ChatGPT with the word and generates a json containing the following:
```json
{
  "word": "李子",
  "pinyin": "lǐzi",
  "definition": "plum",
  "part_of_speech": "noun",
  "example_sentence": "我喜欢吃李子。",
  "example_pinyin": "Wǒ xǐhuān chī lǐzi.",
  "example_translation": "I like to eat plums.",
  "word_audio_path": "PATH_TO_WORD.mp3",
  "sentence_audio_path": "PATH_TO_SENTENCE.mp3"
}
```
2. Calls Google Cloud TTS to generate an MP3 for the word itself and for the example sentence
3. Create a flashcard using the HSK model and inserts it into my Anki Deck