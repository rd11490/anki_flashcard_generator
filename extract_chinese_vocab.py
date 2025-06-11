from app_secrets import chat_gpt_key
from openai import OpenAI
import json

client = OpenAI(api_key=chat_gpt_key)

def extract_chinese_vocab(text):
    prompt = f"""
    Extract all unique Chinese vocabulary words from the following text. Return them as a single comma-separated list, with no duplicates, and no extra explanation or formatting. Strictly return only the list.
    Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for learning Chinese."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=250
    )
    jsn = json.loads(response.model_dump_json())
    chat_resp = jsn['choices'][0]['message']['content']
    return chat_resp.strip()
