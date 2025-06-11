from time import sleep
import requests
from urllib.parse import urlencode
from app_secrets import lazy_chinese_user_id
import os
from extract_chinese_vocab import extract_chinese_vocab
import argparse
from build_from_du_cn import get_cards_from_deck
from build_flashcard import build_flash_card
import shutil
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.lazychinese.com/',
    'Origin': 'https://www.lazychinese.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=4',
}

def fetch_lazy_chinese_videos(number=200, levels='1,2,3', **kwargs):
    """
    Fetch videos from Lazy Chinese API.
    :param number: Number of videos to fetch (default 200)
    :param levels: Comma-separated string of levels (default '1,2,3')
    :param kwargs: Additional query parameters
    :return: List of video dicts (or None if failed)
    """
    base_url = 'https://lazychinese-f9f7g6b5hggwddfj.uksouth-01.azurewebsites.net/GetVideos'
    params = {
        'Number': str(number),
        'Levels': levels,
        'Teachers': '',
        'Tags': '',
        'User': lazy_chinese_user_id,
    }
    params.update(kwargs)
    url = f"{base_url}?{urlencode(params)}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def download_lazy_chinese_mp3(video_id):
    """
    Download the mp3 file for a given video_id from Lazy Chinese and store it in lazy_cn_videos/<video_id>/<video_id>.mp3
    """
    base_dir = 'lazy_cn_videos'
    video_dir = os.path.join(base_dir, str(video_id))
    os.makedirs(video_dir, exist_ok=True)
    mp3_url = f'https://audio.lazychinese.com/{video_id}.mp3'
    mp3_path = os.path.join(video_dir, f'{video_id}.mp3')
    response = requests.get(mp3_url, stream=True)
    if response.status_code == 200:
        with open(mp3_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded mp3 for video {video_id} to {mp3_path}")
    else:
        print(f"Failed to download mp3 for video {video_id}. Status code: {response.status_code}")

def download_lazy_chinese_srt(video_id):
    """
    Download the srt file for a given video_id from Lazy Chinese and store it in lazy_cn_videos/<video_id>/<video_id>.srt
    """
    base_dir = 'lazy_cn_videos'
    video_dir = os.path.join(base_dir, str(video_id))
    os.makedirs(video_dir, exist_ok=True)
    srt_url = f'https://cdn.lazychinese.com/srt/{video_id}.srt'
    srt_path = os.path.join(video_dir, f'{video_id}.srt')
    response = requests.get(srt_url, stream=True)
    if response.status_code == 200:
        with open(srt_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded srt for video {video_id} to {srt_path}")
    else:
        print(f"Failed to download srt for video {video_id}. Status code: {response.status_code}")

def extract_chinese_from_srt(video_id):
    """
    Read the srt file for a given video_id and return all Chinese lines as one large paragraph.
    """
    srt_path = os.path.join('lazy_cn_videos', str(video_id), f'{video_id}.srt')
    if not os.path.exists(srt_path):
        print(f"SRT file not found: {srt_path}")
        return ''
    chinese_lines = []
    with open(srt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines, numbers, and timestamps
            if not line or line.isdigit() or re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
                continue
            # Heuristic: if the line contains any CJK character, keep it
            if re.search(r'[\u4e00-\u9fff]', line):
                chinese_lines.append(line)
    return ''.join(chinese_lines)

def copy_mp3_with_title(video_dir, video_id, title):
    """
    Copy the mp3 file to the same directory with the title as the filename (sanitized).
    """
    mp3_path = os.path.join(video_dir, f'{video_id}.mp3')
    if os.path.exists(mp3_path):
        safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
        title_mp3_path = os.path.join(video_dir, f'{safe_title}.mp3')
        if not os.path.exists(title_mp3_path):
            shutil.copy(mp3_path, title_mp3_path)
            print(f"Copied mp3 to {title_mp3_path}")

def ensure_video_data_downloaded(video, force=False):
    """
    Ensure the directory for the video exists and the mp3 and srt files are downloaded.
    Only download if the file does not already exist, unless force is True.
    Also copy the mp3 to the same directory with the title as the filename.
    """

    video_id = video['id']
    title = video['title']
    base_dir = 'lazy_cn_videos'
    video_dir = os.path.join(base_dir, str(video_id))
    os.makedirs(video_dir, exist_ok=True)
    file_types = {
        'mp3': download_lazy_chinese_mp3,
        'srt': download_lazy_chinese_srt,
    }
    for ext, download_func in file_types.items():
        file_path = os.path.join(video_dir, f'{video_id}.{ext}')
        if force or not os.path.exists(file_path):
            download_func(video_id)
        else:
            print(f"{ext.upper()} already exists for video {video_id}")
    copy_mp3_with_title(video_dir, video_id, title)

# Support query params from command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and process Lazy Chinese videos.")
    parser.add_argument('-n', '--number', type=int, default=200, help='Number of videos to fetch (default: 200)')
    parser.add_argument('-l', '--levels', type=str, default='1,2,3', help='Comma-separated string of levels (default: 1,2,3)')
    parser.add_argument('-f', '--force', action='store_true', help='Force download even if files already exist')
    args = parser.parse_args()

    data = fetch_lazy_chinese_videos(number=args.number, levels=args.levels)
    if data is not None:
        print(f"Response received successfully. Number of videos: {len(data)}")
        vocab_set = set()
        for video in data:
            print(f"Title: {video['title']}, id: {video['id']}")
            ensure_video_data_downloaded(video, force=args.force)
            chinese_text = extract_chinese_from_srt(video['id'])
            print(f"Extracted Chinese text: {chinese_text}")
            vocab_str = extract_chinese_vocab(chinese_text)
            vocab_list = [w.strip() for w in vocab_str.split(',') if w.strip()]
            vocab_set.update(vocab_list)
            sleep(3)  # Sleep to avoid overwhelming the server
        print(f"Combined vocab list across all videos: {sorted(vocab_set)}")

    # Now check for any words in vocab_set that are not already in the anki deck and create cards for them
    deck_name = "targeted_study"
    cards = get_cards_from_deck(deck_name)
    card_list = []
    for card in cards:
        word = card['fields']['Simplified']['value']
        card_list.append(word.strip())
    print(f"Found {len(card_list)} existing cards in deck '{deck_name}'")
    cards_to_create = []
    for word in vocab_set:
        if word not in card_list:
            cards_to_create.append(word)
        else:
            print(f"Skipping existing word: {word}")
    for word in cards_to_create:
        print(word)
        try:
            build_flash_card(word, 'targeted_study')
        except Exception as e:
            print(f'Could not create card for {word}: {e}')
