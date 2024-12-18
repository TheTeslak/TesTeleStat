import json
from collections import Counter

def format_number(number):
    s = str(int(number))
    parts = []
    for i in range(len(s), 0, -3):
        parts.append(s[max(i - 3, 0):i])
    parts.reverse()
    return ' '.join(parts)

def generate_text_report(analysis_results, config, current_texts, output_filename, author_github_link, author_telegram_channel, is_personal_chat):
    day_localization = ('day_names' in current_texts and isinstance(current_texts['day_names'], dict) and 'ru' in current_texts['day_names'] and len(current_texts['day_names']['ru']) > 0)
    month_localization = ('month_names' in current_texts and isinstance(current_texts['month_names'], dict) and 'ru' in current_texts['month_names'] and len(current_texts['month_names']['ru']) > 0)

    def localize_day(d):
        if day_localization:
            ru_days = current_texts['day_names']['ru']
            lang_keys = list(current_texts['day_names'].keys())
            current_lang = 'en' if 'en' in lang_keys else lang_keys[0]
            target_days = current_texts['day_names'].get(current_lang, ru_days)
            if d in ru_days:
                idx = ru_days.index(d)
                return target_days[idx]
        return d

    def localize_month(m):
        if month_localization:
            ru_months = current_texts['month_names']['ru']
            lang_keys = list(current_texts['month_names'].keys())
            current_lang = 'en' if 'en' in lang_keys else lang_keys[0]
            target_months = current_texts['month_names'].get(current_lang, ru_months)
            parts = m.split()
            if len(parts) == 2:
                month_ru = parts[0]
                year_str = parts[1]
                if month_ru in ru_months:
                    m_idx = ru_months.index(month_ru)
                    return f"{target_months[m_idx].capitalize()} {year_str}"
        return m

    first_date = analysis_results.get('first_date', None)
    last_date = analysis_results.get('last_date', None)
    date_range_str = ''
    if first_date and last_date:
        period_label = current_texts.get('date_range_for', '')
        if period_label:
            date_range_str = f"{period_label}: {first_date.strftime('%d.%m.%Y')} – {last_date.strftime('%d.%m.%Y')}"
        else:
            date_range_str = f"{first_date.strftime('%d.%m.%Y')} – {last_date.strftime('%d.%m.%Y')}"

    chat_name = analysis_results.get('chat_name', current_texts.get('no_name','Name'))
    chat_type = analysis_results.get('type', 'group')

    if 'channel' in chat_type:
        title_line = current_texts['channel_statistics'].format(chat_name, date_range_str)
    else:
        title_line = current_texts['chat_statistics'].format(chat_name, date_range_str)

    author_post_count = analysis_results.get('author_post_count', Counter())
    posts_by_date = analysis_results.get('posts_by_date', {})

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(title_line + "\n\n")
        f.write(current_texts['chat_name_label'] + " " + chat_name + "\n")
        f.write(current_texts['type_label'] + " " + chat_type + "\n\n")

        total_msgs = analysis_results['total_messages']
        total_symbols = analysis_results['total_symbols']
        avg_message_length = analysis_results['avg_message_length']

        f.write(config['emojis']['messages'] + " " + current_texts['messages_label'].format(format_number(total_msgs)) + "\n")
        f.write(config['emojis']['symbols'] + " " + current_texts['symbols_label'].format(format_number(total_symbols)) + "\n")
        f.write(config['emojis']['avg_symbols'] + " " + current_texts['average_message_length'] + f": {avg_message_length:.0f}\n\n")

        mc = analysis_results['message_counts']
        f.write(config['emojis'].get('pictures','') + " " + current_texts['pictures'] + ": " + format_number(mc['picture']) + "\n")
        f.write(config['emojis'].get('videos','') + " " + current_texts['videos'] + ": " + format_number(mc['video']) + "\n")
        f.write(config['emojis'].get('files','') + " " + current_texts['files'] + ": " + format_number(mc['file']) + "\n")
        f.write(config['emojis'].get('audios','') + " " + current_texts['audios'] + ": " + format_number(mc['audio']) + "\n")
        f.write(config['emojis'].get('links','') + " " + current_texts['links'] + ": " + format_number(mc['links']) + "\n")
        f.write(config['emojis'].get('voice','') + " " + current_texts['voice_messages'] + ": " + format_number(mc['voice_message']) + "\n")
        f.write(config['emojis'].get('gif','') + " GIF: " + format_number(mc['gif']) + "\n")
        f.write(config['emojis'].get('sticker','') + " " + current_texts['stickers'] + ": " + format_number(mc['sticker']) + "\n")
        f.write(config['emojis'].get('emoji','') + " " + current_texts['emojis'] + ": " + format_number(mc['emojis']) + "\n")
        f.write(config['emojis'].get('poll','') + " " + current_texts['polls'] + ": " + format_number(mc['poll']) + "\n")
        f.write(config['emojis'].get('command','') + " " + current_texts['commands'] + ": " + format_number(mc['commands']) + "\n")
        f.write(config['emojis'].get('profanity','') + " " + current_texts['profanity_messages'] + ": " + format_number(mc['profanity']) + "\n\n")

        if 'channel' in chat_type:
            if author_post_count:
                f.write(current_texts['authors_by_posts'] + "\n")
                top_authors = author_post_count.most_common()
                for author, count in top_authors:
                    f.write(f"{author}: {format_number(count)}\n")
                f.write("\n")

            if posts_by_date:
                f.write(current_texts['posts_by_month_and_author'] + "\n")
                for month, authors_cnt in posts_by_date.items():
                    f.write(f"{month}:\n")
                    for author, cnt in authors_cnt.items():
                        f.write(f"  {author}: {format_number(cnt)}\n")
                f.write("\n")

        if chat_type == 'personal_chat':
            participants = list(analysis_results['user_counts'].keys())
            if len(participants) == 2:
                u_counts = analysis_results['user_counts']
                ncc = analysis_results['non_consecutive_counts']
                user1, user2 = participants
                c1 = u_counts[user1]
                c2 = u_counts[user2]
                nc1 = ncc[user1]
                nc2 = ncc[user2]
                if 'personal_chat_stats' in current_texts:
                    stats_str = current_texts['personal_chat_stats'].format(
                        user1,
                        format_number(c1),
                        format_number(nc1),
                        user2,
                        format_number(c2),
                        format_number(nc2)
                    )
                    f.write(stats_str + "\n")

                total_symbols_all = analysis_results['total_symbols']
                total_reading_seconds = (total_symbols_all / 1000) * 60
                total_reading_minutes = int(total_reading_seconds / 60)
                total_reading_hours = int(total_reading_minutes / 60)
                total_reading_days = total_reading_hours / 24
                days_part = ""
                if total_reading_days >= 1:
                    days_part = current_texts['days'].format(f"{total_reading_days:.2f}")
                read_str = current_texts['reading_time_estimate'].format(
                    int(total_reading_seconds),
                    total_reading_minutes,
                    total_reading_hours,
                    days_part
                )
                f.write("\n" + read_str + "\n")
        elif 'channel' not in chat_type:
            p_emoji = config['emojis'].get('participant', '')
            f.write(p_emoji + " " + current_texts['top_participants'] + ":\n")
            sorted_users = analysis_results['user_counts'].most_common(config.get('top_participants_count'))
            rank = 1
            show_links = config.get('show_user_links', False)
            for user, ucount in (sorted_users if sorted_users else []):
                non_consecutive_count = analysis_results['non_consecutive_counts'][user]
                symbols_val = analysis_results['user_symbols'][user]
                non_consecutive_symbols_val = analysis_results['non_consecutive_symbols'][user]
                user_id = analysis_results['user_ids'].get(user, '')
                if config.get('show_non_consecutive_counts', True):
                    if show_links and user_id:
                        f.write(f"{rank}. {user} (tg://openmessage?user_id={user_id}):\n")
                    else:
                        f.write(f"{rank}. {user}:\n")
                    f.write(
                        f"—— {format_number(ucount)} · {format_number(symbols_val)} {current_texts.get('or_word','or')} "
                        f"({format_number(non_consecutive_count)}) · ({format_number(non_consecutive_symbols_val)})\n"
                    )
                else:
                    if show_links and user_id:
                        f.write(f"{rank}. {user} (tg://openmessage?user_id={user_id}):\n")
                    else:
                        f.write(f"{rank}. {user}:\n")
                    f.write(f"{format_number(ucount)} · {format_number(symbols_val)}\n")
                rank += 1
            f.write("\n")

        else:
            top_emojis = analysis_results['top_emojis']
            if top_emojis:
                f.write(current_texts['top_reactions'] + "\n")
                rank = 1
                for emoji, count in top_emojis:
                    f.write(f"{rank}. {emoji}: {format_number(count)}\n")
                    rank += 1
                f.write("\n")

            top_posts = analysis_results['top_posts_by_reactions']
            if top_posts:
                f.write(current_texts['top_posts_by_reactions'] + "\n")
                rank = 1
                for mid, rcount in top_posts[:10]:
                    f.write(f"{rank}. message_id {mid}: {format_number(rcount)}\n")
                    rank += 1
                f.write("\n")

        w_emoji = config['emojis'].get('word', '')
        f.write(w_emoji + " " + current_texts['top_words'] + ":\n")
        rank = 1
        for wval, freq in analysis_results['common_words']:
            f.write(f"{rank}. {wval}: {format_number(freq)}\n")
            rank += 1
        f.write("\n")

        ph_emoji = config['emojis'].get('phrase', '')
        f.write(ph_emoji + " " + current_texts['top_phrases'] + ":\n")
        rank = 1
        for phrase, freq in analysis_results['common_phrases']:
            f.write(f"{rank}. {phrase}: {format_number(freq)}\n")
            rank += 1
        f.write("\n")

        a_emoji = config['emojis'].get('activity', '')
        f.write(a_emoji + " " + current_texts['activity'] + ":\n")
        activity_data = analysis_results['activity']
        hours_str = ', '.join([
            f"{config['emojis'].get('list_item', '')} {hour}:00–{hour}:59"
            for hour, _ in activity_data['hours']
        ])
        f.write(hours_str + "\n")

        localized_weekdays = []
        if day_localization:
            ru_days = current_texts['day_names']['ru']
            lang_keys = list(current_texts['day_names'].keys())
            current_lang = 'en' if 'en' in lang_keys else lang_keys[0]
            target_days = current_texts['day_names'].get(current_lang, ru_days)
            for weekday, _ in activity_data['weekdays']:
                if weekday in ru_days:
                    idx = ru_days.index(weekday)
                    localized_weekdays.append(f"{config['emojis'].get('list_item', '')} {target_days[idx]}")
                else:
                    localized_weekdays.append(f"{config['emojis'].get('list_item', '')} {weekday}")
        else:
            for weekday, _ in activity_data['weekdays']:
                localized_weekdays.append(f"{config['emojis'].get('list_item', '')} {weekday}")
        f.write(', '.join(localized_weekdays) + "\n")

        localized_months = []
        if month_localization:
            ru_months = current_texts['month_names']['ru']
            lang_keys = list(current_texts['month_names'].keys())
            current_lang = 'en' if 'en' in lang_keys else lang_keys[0]
            target_months = current_texts['month_names'].get(current_lang, ru_months)
            for m, _ in activity_data['months']:
                parts = m.split()
                if len(parts) == 2:
                    month_ru = parts[0]
                    year_str = parts[1]
                    if month_ru in ru_months:
                        m_idx = ru_months.index(month_ru)
                        localized_months.append(f"{config['emojis'].get('list_item', '')} {target_months[m_idx].capitalize()} {year_str}")
                    else:
                        localized_months.append(f"{config['emojis'].get('list_item', '')} {m}")
                else:
                    localized_months.append(f"{config['emojis'].get('list_item', '')} {m}")
        else:
            for m, _ in activity_data['months']:
                localized_months.append(f"{config['emojis'].get('list_item', '')} {m}")
        f.write(', '.join(localized_months) + "\n")

        years_str = ', '.join([
            f"{config['emojis'].get('list_item', '')} {year}"
            for year, _ in activity_data['years']
        ])
        f.write(years_str + "\n\n")

        mad_text = current_texts['most_active_days']
        f.write(a_emoji + " " + mad_text + ":\n")
        ds = analysis_results.get('date_symbols', {})
        rank = 1
        for date_val, msg_count in analysis_results['top_days']:
            symbol_count = ds.get(date_val,0)
            avg_len = symbol_count / msg_count if msg_count else 0
            date_str = date_val.strftime('%d.%m.%Y')
            f.write(
                f"{rank}. {date_str}: {config['emojis'].get('messages','')} {format_number(msg_count)}, "
                f"{config['emojis'].get('symbols','')} {format_number(symbol_count)}, {config['emojis'].get('avg_symbols','')} {avg_len:.1f}\n"
            )
            rank += 1
        f.write("\n")

        if analysis_results.get('creator_name') and analysis_results.get('creator_id'):
            creator_info_str = current_texts['creator_info'].format(
                analysis_results['creator_name'],
                analysis_results['creator_id']
            )
            f.write(creator_info_str + "\n")

        if config.get('show_author_links', True):
            f.write('\n\n⚡️\n')
            f.write(current_texts['author_links'].format(author_github_link, author_telegram_channel))
            f.write('\n⚡️\n')

def generate_json_report(analysis_results, json_output_filename):
    json_output_data = {}
    with open(json_output_filename, 'w', encoding='utf-8') as jf:
        json.dump(json_output_data, jf, ensure_ascii=False, indent=4)