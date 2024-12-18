import datetime
import ijson
import json
import re
import os

def load_json_header(input_file):
    # This function extracts only the header fields (name, type, id) from the JSON file
    # using a streaming parser without loading the entire file.
    header_fields = ['name', 'type', 'id']
    header_data = {}
    with open(input_file, 'r', encoding='utf-8') as f:
        parser = ijson.parse(f)
        current_field = None
        for prefix, event, value in parser:
            if prefix == '' and event == 'map_key':
                current_field = value
            elif current_field in header_fields and event in ('string', 'number'):
                header_data[current_field] = value
            if all(field in header_data for field in header_fields):
                break
    return header_data

def load_json_file(input_file):
    # Loads the entire JSON data into memory.
    # Useful for smaller files or when we need all messages at once.
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def parse_messages_streaming(input_file):
    # Streams through messages without loading all at once.
    # This approach helps handle large JSON exports more efficiently.
    with open(input_file, 'r', encoding='utf-8') as f:
        messages = ijson.items(f, 'messages.item')
        for message in messages:
            if message is not None:
                yield message

def is_bot(user_name, bot_identifiers):
    # Checks if a user name contains a known bot identifier.
    return any(bot_id.lower() in user_name.lower() for bot_id in bot_identifiers)

def format_number(number):
    # Formats an integer with spacing between every three digits for readability.
    s = str(int(number))
    parts = []
    for i in range(len(s), 0, -3):
        parts.append(s[max(i - 3, 0):i])
    parts.reverse()
    return ' '.join(parts)

def load_word_list(file_path):
    # Loads words from a given file into a set, one word per line.
    words = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    words.add(w)
    return words