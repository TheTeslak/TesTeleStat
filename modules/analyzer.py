import datetime
from collections import Counter, defaultdict
import re
import os
import ijson
import json

def is_bot(user_name, bot_identifiers):
    # Check if the username contains any known bot identifier.
    # This helps exclude bot accounts from participant statistics if configured.
    return any(bot_id.lower() in user_name.lower() for bot_id in bot_identifiers)

def format_number(number):
    # Inserts spaces as thousand separators for readability.
    s = str(int(number))
    parts = []
    for i in range(len(s), 0, -3):
        parts.append(s[max(i - 3, 0):i])
    parts.reverse()
    return ' '.join(parts)

def load_word_list(file_path):
    # Loads words from a file into a set. Used for stop words and profanity lists.
    words = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    words.add(w)
    return words

def analyze_messages(input_file, config, current_texts, is_personal_chat, use_streaming=False, start_date=None, end_date=None, language='en'):
    # This function processes messages, counting frequencies, words, media, etc.
    # The complexity lies in streaming large JSON files and selectively processing messages.
    # 'language' parameter is used to choose day and month names from config.

    if use_streaming:
        # Streaming parsing prevents loading the entire JSON into memory at once.
        # This is crucial for very large exports.
        messages = parse_messages_streaming(input_file)
        header_data = load_json_header(input_file)
        chat_name = header_data.get('name', 'Chat Name')
    else:
        data = load_json_file(input_file)
        messages = data.get('messages', [])
        total_messages = len(messages)
        print(current_texts['total_messages'].format(format_number(total_messages)))
        if total_messages == 0:
            return {}, {'errors': [], 'unprocessed_messages': 0}
        chat_name = data.get('name', 'Chat Name')

    # Select day and month names based on chosen language. Defaults to English if not found.
    day_names_list = config['day_names'].get(language, config['day_names']['en'])
    month_names_list = config['month_names'].get(language, config['month_names']['en'])

    user_counts = Counter()
    user_symbols = Counter()
    non_consecutive_counts = Counter()
    non_consecutive_symbols = Counter()
    user_ids = {}
    prev_user = None
    prev_time = None
    words = []
    phrases_2 = []
    phrases_3 = []
    hours = Counter()
    weekdays = Counter()
    months = Counter()
    years = Counter()
    dates = Counter()
    date_messages = defaultdict(int)
    date_symbols = defaultdict(int)
    daily_user_messages = defaultdict(lambda: Counter())
    daily_first_sender = {}
    daily_user_non_consecutive_messages = defaultdict(lambda: Counter())
    invite_counts = Counter()
    creator_name = None
    creator_id = None
    includes_media = 0
    chain_started = False

    words_dir = config.get('words_dir', 'words')
    stop_words_type = config.get('stop_words_type', 'minimal')
    stop_words_file = os.path.join(words_dir, f'stop_words_{stop_words_type}.txt')
    profanity_words_file = os.path.join(words_dir, 'profanity_words.txt')

    stop_words = load_word_list(stop_words_file)
    english_stop_words_file = os.path.join(words_dir, 'stop_words_english.txt')
    english_stop_words = load_word_list(english_stop_words_file)
    stop_words.update(english_stop_words)

    # If no stop words are found, use a basic default set.
    if not stop_words:
        stop_words = set(['и','в','не','на','с','что','а','как','это','по','но','из','у','за','о','же','то','к','для','до','вы','мы',
                          'они','он','она','оно','так','было','только','бы','когда','уже','ли','или','со','a','the','and','or','but',
                          'if','in','on','with','for','is','was','are','were','be','to','of','at','by','an'])

    profanity_words = load_word_list(profanity_words_file)

    commands_identifiers = set(config.get('commands_identifiers', ['/']))
    emoji_pattern = config['emoji_pattern']
    url_pattern = config['url_pattern']

    message_counts = {
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

    first_date = None
    last_date = None

    unprocessed_messages = 0
    error_count = 0
    errors = []

    # Spinner is used to show some progress indication without a complex progress bar.
    spinner = ['|', '/', '-', '\\']
    spinner_index = 0

    def print_progress(current):
        # Prints a lightweight progress indicator showing how many messages have been processed.
        nonlocal spinner_index
        current_formatted = format_number(current)
        symbol = spinner[spinner_index % len(spinner)]
        spinner_index += 1
        progress = current_texts['processing'].format(current_formatted, symbol)
        print(progress, end='\r', flush=True)

    first_message_interval_seconds = config.get('first_message_interval_hours', 1) * 3600
    time_offset = config.get('time_offset', 0)
    time_offset_delta = datetime.timedelta(hours=time_offset)

    total_messages_processed = 0

    for message in messages:
        total_messages_processed += 1

        if message is None or message.get('type') != 'message':
            prev_user = None
            continue

        try:
            if 'text' not in message:
                prev_user = None
                continue

            user = message.get('from', '') or message.get('actor', 'Unknown')
            from_id = message.get('from_id', '') or message.get('actor_id', '') or message.get('id', '')
            if from_id:
                # Standardizing user_id extraction, as Telegram exports may have strings like 'user123'.
                if isinstance(from_id, str):
                    if from_id.startswith('user'):
                        user_id = from_id.replace('user', '')
                    elif from_id.startswith('channel'):
                        user_id = from_id.replace('channel', '')
                    else:
                        user_id = from_id
                else:
                    user_id = str(from_id)
                user_ids[user] = user_id
            else:
                user_id = ''
                user_ids[user] = user_id

            if not is_personal_chat and config.get('exclude_bots', True) and is_bot(user, config.get('bot_identifiers', [])):
                # Skip bot messages if configured to exclude bots in a group chat.
                prev_user = user
                continue

            text = message['text']
            if isinstance(text, list):
                # Telegram exports sometimes break messages into a list with text and formatting objects.
                # We reconstruct the full message text by concatenating all parts.
                text_pieces = []
                for t_piece in text:
                    if isinstance(t_piece, dict):
                        text_pieces.append(t_piece.get('text', ''))
                    elif isinstance(t_piece, str):
                        text_pieces.append(t_piece)
                text = ''.join(text_pieces)
            elif text is None:
                text = ''

            symbols = len(text)
            user_counts[user] += 1
            user_symbols[user] += symbols

            # non_consecutive_counts track the number of times a user appears after a different user,
            # providing an alternative metric for participant dynamics.
            if prev_user != user:
                non_consecutive_counts[user] += 1
                non_consecutive_symbols[user] += symbols
                chain_started = True
            else:
                chain_started = False

            message_date = message.get('date')
            if message_date:
                try:
                    date_time = datetime.datetime.fromisoformat(message_date)
                    # Adjust times by offset if configured.
                    date_time += time_offset_delta
                    if start_date and end_date:
                        # If a date range is specified, skip messages outside this range.
                        if not (start_date.date() <= date_time.date() <= end_date.date()):
                            prev_user = user
                            prev_time = date_time
                            continue
                    if first_date is None or date_time < first_date:
                        first_date = date_time
                    if last_date is None or date_time > last_date:
                        last_date = date_time

                    date_only = date_time.date()

                    if is_personal_chat:
                        # In personal chats, we also track daily user messages for detailed analysis.
                        daily_user_messages[date_only][user] += 1
                        if prev_user != user:
                            daily_user_non_consecutive_messages[date_only][user] += 1
                        # daily_first_sender determines who started talking after a break each day.
                        if date_only not in daily_first_sender or (prev_time and (date_time - prev_time).total_seconds() > first_message_interval_seconds):
                            daily_first_sender[date_only] = user

                    date_messages[date_only] += 1
                    date_symbols[date_only] += symbols
                    hours[date_time.hour] += 1

                    # Use language-appropriate day and month names.
                    weekday_index = date_time.weekday()
                    weekday_name = day_names_list[weekday_index]
                    weekdays[weekday_name] += 1
                    month_name = f"{month_names_list[date_time.month -1]} {date_time.year}"
                    months[month_name] += 1
                    years[date_time.year] += 1
                    dates[date_only] += 1
                except (ValueError, KeyError) as e:
                    # If date parsing fails, record the error and skip the message.
                    error_count += 1
                    errors.append(f"Error processing date in message id {message.get('id')}: {e}\n")
                    prev_time = None
            else:
                prev_time = None

            prev_user = user
            if 'date_time' in locals():
                prev_time = date_time

            if text:
                # Clean text to identify words for frequency counts.
                text_clean = re.sub(r'[^\w\s]', '', text.lower())
                words_in_text = [w for w in text_clean.split() if w.isalpha()]

                # Remove stop words, leaving only meaningful words for frequency analysis.
                words_filtered = [w for w in words_in_text if w not in stop_words]

                # Track common phrases of 2 and 3 words length.
                for i in range(len(words_filtered) - 1):
                    phrase_2 = f"{words_filtered[i]} {words_filtered[i+1]}"
                    phrases_2.append(phrase_2)
                    if i < len(words_filtered) - 2:
                        phrase_3 = f"{words_filtered[i]} {words_filtered[i+1]} {words_filtered[i+2]}"
                        phrases_3.append(phrase_3)

                words.extend([w for w in words_in_text if w not in stop_words])

                # Count commands (messages starting with '/', typical for Telegram bot commands).
                if text.strip().startswith(tuple(commands_identifiers)):
                    message_counts['commands'] += 1

                # Check if message contains emojis.
                if emoji_pattern.search(text):
                    message_counts['emojis'] += 1

                # Check for profanity.
                text_lower = text.lower()
                if any(pw in text_lower for pw in profanity_words):
                    message_counts['profanity'] += 1

                # Check for links/URLs.
                if url_pattern.search(text):
                    message_counts['links'] += 1

            if 'forwarded_from' in message:
                message_counts['forwards'] += 1

            if 'reply_to_message_id' in message:
                message_counts['replies'] += 1

            # Identify message type by 'media_type' or other fields.
            # This classification helps understand content type distribution.
            if 'media_type' in message:
                media_type = message['media_type']
                mime_type = message.get('mime_type', '')
                if media_type == 'sticker':
                    message_counts['sticker'] += 1
                    includes_media += 1
                elif media_type == 'photo':
                    message_counts['picture'] += 1
                    includes_media += 1
                elif media_type == 'video_file':
                    file_name = message.get('file', '') or message.get('file_name', '')
                    if 'gif' in file_name.lower():
                        message_counts['gif'] += 1
                    else:
                        message_counts['video'] += 1
                    includes_media += 1
                elif media_type in ('voice_message', 'video_message'):
                    message_counts['voice_message'] += 1
                    includes_media += 1
                elif media_type == 'audio_file':
                    message_counts['audio'] += 1
                    includes_media += 1
                elif media_type == 'document':
                    message_counts['file'] += 1
                    includes_media += 1
                elif media_type == 'animation':
                    message_counts['gif'] += 1
                    includes_media += 1
                elif media_type == 'poll':
                    message_counts['poll'] += 1
                else:
                    includes_media += 1
            else:
                # If no media_type is given but there's 'photo', count as picture.
                # Otherwise just a text message.
                if 'photo' in message:
                    message_counts['picture'] += 1
                    includes_media += 1
                elif 'file' in message:
                    message_counts['file'] += 1
                    includes_media += 1
                else:
                    message_counts['text'] += 1

        except Exception as e:
            # If any unexpected error occurs, mark this message as unprocessed.
            unprocessed_messages += 1
            error_count += 1
            msg_id = message.get('id', 'Unknown') if isinstance(message, dict) else 'Unknown'
            errors.append(f"Error processing message id {msg_id}: {e}\n")
            prev_user = None
            continue

        if total_messages_processed % 1000 == 0:
            print_progress(total_messages_processed)

    print_progress(total_messages_processed)
    print('\n')

    total_msgs = sum(user_counts.values())
    if total_msgs == 0:
        # No messages processed successfully, return empty results.
        return {}, {'errors': errors, 'unprocessed_messages': 0}

    print(current_texts['total_messages'].format(format_number(total_msgs)))

    total_symbols = sum(user_symbols.values())
    total_non_consecutive_msgs = sum(non_consecutive_counts.values())
    total_non_consecutive_symbols = sum(non_consecutive_symbols.values())
    avg_message_length = total_symbols / total_msgs if total_msgs else 0
    common_words = Counter(words).most_common(config.get('top_words_count', 100))
    common_phrases = Counter(phrases_2 + phrases_3).most_common(config.get('top_phrases_count', 100))
    activity = {
        'hours': hours.most_common(3) if hours else [],
        'weekdays': weekdays.most_common(3) if weekdays else [],
        'months': months.most_common(3) if months else [],
        'years': years.most_common(3) if years else [],
    }
    top_days = dates.most_common(config.get('top_days_count', 10))

    analysis_results = {
        'chat_name': chat_name,
        'total_messages': total_msgs,
        'total_symbols': total_symbols,
        'total_non_consecutive_messages': total_non_consecutive_msgs,
        'total_non_consecutive_symbols': total_non_consecutive_symbols,
        'user_counts': user_counts,
        'user_symbols': user_symbols,
        'non_consecutive_counts': non_consecutive_counts,
        'non_consecutive_symbols': non_consecutive_symbols,
        'user_ids': user_ids,
        'first_date': first_date,
        'last_date': last_date,
        'avg_message_length': avg_message_length,
        'common_words': common_words,
        'common_phrases': common_phrases,
        'activity': activity,
        'top_days': top_days,
        'message_counts': message_counts,
        'invite_counts': invite_counts,
        'creator_name': creator_name,
        'creator_id': creator_id,
        'date_symbols': date_symbols,
        'includes_media': includes_media,
        'dates': dates,
        'date_messages': date_messages,
        'daily_user_messages': daily_user_messages,
        'daily_first_sender': daily_first_sender,
        'daily_user_non_consecutive_messages': daily_user_non_consecutive_messages,
    }

    error_info = {
        'errors': errors,
        'unprocessed_messages': unprocessed_messages,
    }

    return analysis_results, error_info

def parse_messages_streaming(input_file):
    # Yields messages one by one from a potentially large JSON file using ijson.
    # This allows processing large exports without loading them fully into RAM.
    with open(input_file, 'r', encoding='utf-8') as f:
        messages = ijson.items(f, 'messages.item')
        for message in messages:
            if message is not None:
                yield message

def load_json_header(input_file):
    # Loads only header fields like 'name', 'type', 'id' from the file.
    # We stop as soon as we have the needed fields to avoid reading the entire file.
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
    # Loads the entire JSON file into memory. Not recommended for very large exports.
    # Streaming methods are preferred, but this fallback can be used for smaller files.
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data