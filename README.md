# anki_flashcard_generator
Auto generates anki flashcards using chatgpt and google cloud tts

##### NOTE:
This project is currently not generalized to match multiple languages, decks, etc. It was built for my specific use case


#### To Create New Cards
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


#### To Create Temporary Deck for Targeted Study
```commandline
python targeted_study.py -d targeted_study -w 无尾熊,树,根,吸,金子,叶子,卡,来自,介绍,植物,这种,黄金,钱,地方,附近,有可能,石竹
```
This will build a new deck using only the desired words

#### To Reset the Temporary Deck
```commandline
python targeted_study.py -d newbie_lazy_cn_deck -s targeted_study -r 
```
This will move all cards from the source deck to the destination deck.

| Argument        | Short Form | Description                                             | Required |
|-----------------|------------|---------------------------------------------------------|----------|
| `--deck`        | `-d`       | Name of the destination deck                            | ✅        |
| `--words`       | `-w`       | Words to use to create the deck                         | ❌        |
| `--source-deck` | `-s`       | The Deck from which the cards are being moved (-r only) | ❌        |
| `--reset`       | `-r`       | Reset the deck                                          | ❌        |


