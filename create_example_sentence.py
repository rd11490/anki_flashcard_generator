import openai
from secrets import chat_gpt_key
from openai import OpenAI
import json

client = OpenAI(api_key=chat_gpt_key)


def generate_chinese_sentence(word):
    prompt = f"""
       For the Chinese word “{word}”, provide the following information in JSON format:
       {{
           "word": "{word}",
           "pinyin": "",  // Include tone marks (e.g., wánměi)
           "definition": "",  // English definition
           "part_of_speech": "", // Part of speech
           "example_sentence": "",  // A slightly complicated conversational Chinese sentence using the word
           "example_pinyin": "",  // Pinyin of the example sentence with tone marks
           "example_translation": ""  // English translation of the example sentence
       }}
        Strictly return only the JSON object, nothing else.
       """


    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant for learning Chinese."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,  # Adjust for more creative responses if needed
        max_tokens=250     # Limit response length
    )

    jsn = json.loads(response.model_dump_json())
    print(jsn)
    chat_resp = jsn['choices'][0]['message']['content']
    result = json.loads(chat_resp)
    return result