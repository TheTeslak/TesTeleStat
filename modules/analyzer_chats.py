import datetime
import re
import os
from collections import defaultdict
import collections
from .analyzer_common import parse_messages_streaming, load_word_list, is_bot, format_number
from .analyzer_utils import process_message

def analyze_messages(input_file, config, current_texts, is_personal_chat, use_streaming=False, start_date=None, end_date=None, language='en'):
    if use_streaming:
        messages = parse_messages_streaming(input_file)
        from .analyzer_common import load_json_header
        header_data = load_json_header(input_file)
        chat_name = header_data.get('name', 'Chat Name')
        chat_type = header_data.get('type', 'group')
    else:
        from .analyzer_common import load_json_file
        data = load_json_file(input_file)
        messages = data.get('messages', [])
        total_messages = len(messages)
        print(current_texts['messages_analyzed'].format(format_number(total_messages)))
        if total_messages == 0:
            return {}, {'errors': [], 'unprocessed_messages': 0}
        chat_name = data.get('name', 'Chat Name')
        chat_type = data.get('type', 'group')

    day_names_list = config['day_names'].get(language, config['day_names']['en'])
    month_names_list = config['month_names'].get(language, config['month_names']['en'])

    user_counts = collections.Counter()
    user_symbols = collections.Counter()
    non_consecutive_counts = collections.Counter()
    non_consecutive_symbols = collections.Counter()
    user_ids = {}
    prev_user = None
    prev_time = None
    words = []
    phrases_2 = []
    phrases_3 = []
    hours = collections.Counter()
    weekdays = collections.Counter()
    months = collections.Counter()
    years = collections.Counter()
    dates = collections.Counter()
    date_messages = defaultdict(int)
    date_symbols = defaultdict(int)
    daily_user_messages = defaultdict(lambda: collections.Counter())
    daily_first_sender = {}
    daily_user_non_consecutive_messages = defaultdict(lambda: collections.Counter())
    invite_counts = collections.Counter()
    creator_name = None
    creator_id = None
    includes_media = 0

    emoji_reactions_counter = collections.Counter()
    message_reactions_count = {}

    words_dir = config.get('words_dir', 'words')
    stop_words_type = config.get('stop_words_type', 'minimal')
    stop_words_file = os.path.join(words_dir, f'stop_words_{stop_words_type}.txt')
    profanity_words_file = os.path.join(words_dir, 'profanity_words.txt')
    stop_words = load_word_list(stop_words_file)
    english_stop_words_file = os.path.join(words_dir, 'stop_words_english.txt')
    english_stop_words = load_word_list(english_stop_words_file)
    stop_words.update(english_stop_words)
    if not stop_words:
        stop_words = set(['и','в','не','на','с','что','а','как','это','по','но','из','у','за','о','же','то','к','для','до','вы','мы',
                          'они','он','она','оно','так','было','только','бы','когда','уже','ли','или','со','a','the','and','or','but',
                          'if','in','on','with','for','is','was','are','were','be','to','of','at','by','an'])
    profanity_words = load_word_list(profanity_words_file)

    commands_identifiers = set(config.get('commands_identifiers', []))
    emoji_pattern = config['emoji_pattern']

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
    spinner = ['|', '/', '-', '\\']
    spinner_index = 0

    def print_progress(current):
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
                prev_user = user
                continue

            message_counts_local, words_local, p2_local, p3_local, links_in_message = process_message(
                message, config, stop_words, profanity_words, commands_identifiers, emoji_pattern
            )

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
            symbols = len(text)
            user_counts[user] += 1
            user_symbols[user] += symbols

            if prev_user != user:
                non_consecutive_counts[user] += 1
                non_consecutive_symbols[user] += symbols

            message_date = message.get('date')
            if message_date:
                try:
                    date_time = datetime.datetime.fromisoformat(message_date)
                    date_time += time_offset_delta
                    if start_date and end_date:
                        if not (start_date.date() <= date_time.date() <= end_date.date()):
                            prev_user = user
                            prev_time = date_time
                            for k, v in message_counts_local.items():
                                message_counts[k] += v
                            continue
                    if first_date is None or date_time < first_date:
                        first_date = date_time
                    if last_date is None or date_time > last_date:
                        last_date = date_time

                    date_only = date_time.date()
                    if is_personal_chat:
                        daily_user_messages[date_only][user] += 1
                        if prev_user != user:
                            daily_user_non_consecutive_messages[date_only][user] += 1
                        if date_only not in daily_first_sender or (prev_time and (date_time - prev_time).total_seconds() > first_message_interval_seconds):
                            daily_first_sender[date_only] = user

                    date_messages[date_only] += 1
                    date_symbols[date_only] += symbols
                    hours[date_time.hour] += 1
                    weekday_index = date_time.weekday()
                    weekday_name = day_names_list[weekday_index]
                    weekdays[weekday_name] += 1
                    month_name = f"{month_names_list[date_time.month -1]} {date_time.year}"
                    months[month_name] += 1
                    years[date_time.year] += 1
                    dates[date_only] += 1
                    prev_time = date_time
                except (ValueError, KeyError) as e:
                    error_count += 1
                    msg_id = message.get('id', 'Unknown')
                    errors.append(current_texts['error_processing_date'].format(msg_id, e))
                    prev_time = None
            else:
                prev_time = None

            words.extend(words_local)
            phrases_2.extend(p2_local)
            phrases_3.extend(p3_local)

            for k, v in message_counts_local.items():
                message_counts[k] += v

            reactions = message.get('reactions', [])
            total_reactions_for_message = 0
            for r in reactions:
                if r.get('type') == 'emoji':
                    count = r.get('count', 0)
                    emoji_reactions_counter[r['emoji']] += count
                    total_reactions_for_message += count
            message_reactions_count[message.get('id', 0)] = total_reactions_for_message

            prev_user = user

        except Exception as e:
            unprocessed_messages += 1
            error_count += 1
            msg_id = message.get('id', 'Unknown')
            errors.append(current_texts['error_processing_message'].format(msg_id, e))
            prev_user = None
            continue

        if total_messages_processed % 1000 == 0:
            print_progress(total_messages_processed)

    print_progress(total_messages_processed)
    print('\n')

    total_msgs = sum(user_counts.values())
    if total_msgs == 0:
        return {}, {'errors': errors, 'unprocessed_messages': 0}

    print(current_texts['messages_analyzed'].format(format_number(total_msgs)))

    total_symbols = sum(user_symbols.values())
    total_non_consecutive_msgs = sum(non_consecutive_counts.values())
    total_non_consecutive_symbols = sum(non_consecutive_symbols.values())
    avg_message_length = total_symbols / total_msgs if total_msgs else 0
    from collections import Counter
    all_phrases = phrases_2 + phrases_3
    common_words = Counter(words).most_common(config.get('top_words_count', 100))
    common_phrases = Counter(all_phrases).most_common(config.get('top_phrases_count', 100))
    activity = {
        'hours': hours.most_common(3) if hours else [],
        'weekdays': weekdays.most_common(3) if weekdays else [],
        'months': months.most_common(3) if months else [],
        'years': years.most_common(3) if years else [],
    }
    top_days = dates.most_common(config.get('top_days_count', 10))

    top_emojis = emoji_reactions_counter.most_common()
    top_posts_by_reactions = sorted(message_reactions_count.items(), key=lambda x: x[1], reverse=True)

    analysis_results = {
        'chat_name': chat_name,
        'type': chat_type,
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
        'top_emojis': top_emojis,
        'top_posts_by_reactions': top_posts_by_reactions
    }

    error_info = {
        'errors': errors,
        'unprocessed_messages': unprocessed_messages,
    }

    return analysis_results, error_info