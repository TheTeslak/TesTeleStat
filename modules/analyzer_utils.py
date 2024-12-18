import re

def process_message(message, config, stop_words, profanity_words, commands_identifiers, emoji_pattern):
    # Minimal comments if needed: process a single message and return partial stats.
    message_counts_local = {
        'text': 0,
        'sticker': 0,
        'picture': 0,
        'video': 0,
        'gif': 0,
        'voice_message': 0,
        'audio': 0,
        'file': 0,
        'commands': 0,
        'forwards': 0,
        'emojis': 0,
        'profanity': 0,
        'replies': 0,
        'poll': 0,
        'links': 0,
    }

    words_local = []
    phrases_2_local = []
    phrases_3_local = []
    links_in_message = set()

    text = message.get('text', '')
    if isinstance(text, list):
        text_pieces = []
        for t_piece in text:
            if isinstance(t_piece, dict):
                text_pieces.append(t_piece.get('text', ''))
            elif isinstance(t_piece, str):
                text_pieces.append(t_piece)
        text = ''.join(text_pieces)
    if text is None:
        text = ''

    # links
    text_content = message.get('text', [])
    if isinstance(text_content, list):
        for part in text_content:
            if isinstance(part, dict) and part.get('type') == 'text_link':
                href = part.get('href')
                if href:
                    links_in_message.add(href)
    text_entities = message.get('text_entities', [])
    for entity in text_entities:
        if entity.get('type') == 'text_link':
            href = entity.get('href')
            if href:
                links_in_message.add(href)
    message_counts_local['links'] += len(links_in_message)

    # words, commands, emojis, profanity
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    words_in_text = [w for w in text_clean.split() if w.isalpha()]
    words_filtered = [w for w in words_in_text if w not in stop_words]

    for i in range(len(words_filtered) - 1):
        phrase_2 = f"{words_filtered[i]} {words_filtered[i+1]}"
        phrases_2_local.append(phrase_2)
        if i < len(words_filtered) - 2:
            phrase_3 = f"{words_filtered[i]} {words_filtered[i+1]} {words_filtered[i+2]}"
            phrases_3_local.append(phrase_3)

    words_local.extend([w for w in words_in_text if w not in stop_words])

    if text.strip().startswith(tuple(commands_identifiers)):
        message_counts_local['commands'] += 1
    if emoji_pattern.search(text):
        message_counts_local['emojis'] += 1
    text_lower = text.lower()
    if any(pw in text_lower for pw in profanity_words):
        message_counts_local['profanity'] += 1

    if 'forwarded_from' in message:
        message_counts_local['forwards'] += 1
    if 'reply_to_message_id' in message:
        message_counts_local['replies'] += 1

    # media type
    if 'media_type' in message:
        media_type = message['media_type']
        file_name = message.get('file', '') or message.get('file_name', '')
        if media_type == 'sticker':
            message_counts_local['sticker'] += 1
        elif media_type == 'photo':
            message_counts_local['picture'] += 1
        elif media_type == 'video_file':
            if 'gif' in file_name.lower():
                message_counts_local['gif'] += 1
            else:
                message_counts_local['video'] += 1
        elif media_type in ('voice_message', 'video_message'):
            message_counts_local['voice_message'] += 1
        elif media_type == 'audio_file':
            message_counts_local['audio'] += 1
        elif media_type == 'document':
            message_counts_local['file'] += 1
        elif media_type == 'animation':
            message_counts_local['gif'] += 1
        elif media_type == 'poll':
            message_counts_local['poll'] += 1
        else:
            # count as media if needed
            pass
    else:
        # if no media_type but photo or file keys
        if 'photo' in message:
            message_counts_local['picture'] += 1
        elif 'file' in message:
            message_counts_local['file'] += 1
        else:
            message_counts_local['text'] += 1

    return message_counts_local, words_local, phrases_2_local, phrases_3_local, links_in_message