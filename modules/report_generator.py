import json

def format_number(number):
    s = str(int(number))
    parts = []
    for i in range(len(s), 0, -3):
        parts.append(s[max(i - 3, 0):i])
    parts.reverse()
    return ' '.join(parts)

def generate_text_report(analysis_results, config, current_texts, output_filename, author_github_link, author_telegram_channel, is_personal_chat):
    # Generates a human-readable TXT report with statistics.
    # Includes day and month localization and various activity metrics.

    # day_localization checks if we have localized day/month names in current_texts for language switching.
    day_localization = ('day_names' in current_texts
                        and isinstance(current_texts['day_names'], dict)
                        and 'ru' in current_texts['day_names']
                        and len(current_texts['day_names']['ru']) > 0)
    month_localization = ('month_names' in current_texts
                          and isinstance(current_texts['month_names'], dict)
                          and 'ru' in current_texts['month_names']
                          and len(current_texts['month_names']['ru']) > 0)

    if day_localization and month_localization:
        # Determine which language's arrays to use as target localization.
        # If 'en' available, use that for English; else fallback to the first available set.
        lang_keys = list(current_texts['day_names'].keys())
        current_lang = 'en' if 'en' in lang_keys else lang_keys[0]
        ru_days = current_texts['day_names']['ru']
        ru_months = current_texts['month_names']['ru']
        target_days = current_texts['day_names'].get(current_lang, ru_days)
        target_months = current_texts['month_names'].get(current_lang, ru_months)
    else:
        ru_days = []
        ru_months = []
        target_days = []
        target_months = []

    def localize_day(d):
        # Translate Russian day to target language if needed.
        if day_localization and d in ru_days:
            idx = ru_days.index(d)
            return target_days[idx]
        return d

    def localize_month(m):
        # Translate Russian month to target language if needed.
        if month_localization:
            parts = m.split()
            if len(parts) == 2:
                month_ru = parts[0]
                year_str = parts[1]
                if month_ru in ru_months:
                    m_idx = ru_months.index(month_ru)
                    return f"{target_months[m_idx].capitalize()} {year_str}"
        return m

    with open(output_filename, 'w', encoding='utf-8') as f:
        first_date = analysis_results['first_date']
        last_date = analysis_results['last_date']
        date_range_str = ''
        if first_date and last_date:
            period_label = current_texts.get('date_range_for', 'for the period')
            date_range_str = f"{period_label}: {first_date.strftime('%d.%m.%Y')} – {last_date.strftime('%d.%m.%Y')}"
        chat_name = analysis_results.get('chat_name', 'Chat Name')
        f.write(f"Статистика чата \"{chat_name}\" {date_range_str}\n\n")

        total_msgs_formatted = format_number(analysis_results['total_messages'])
        total_symbols_formatted = format_number(analysis_results['total_symbols'])
        avg_message_length = analysis_results['avg_message_length']
        show_non_consecutive = config.get('show_non_consecutive_counts', True)

        if show_non_consecutive:
            ncm = format_number(analysis_results['total_non_consecutive_messages'])
            ncs = format_number(analysis_results['total_non_consecutive_symbols'])
            f.write(
                f"{config['emojis'].get('messages','')} {current_texts['messages'].capitalize()}: {total_msgs_formatted} "
                f"({ncm} {current_texts.get('non_consecutive', 'not consecutive')})\n"
            )
            f.write(
                f"{config['emojis'].get('symbols','')} {current_texts.get('symbols', 'symbols').capitalize()}: {total_symbols_formatted} "
                f"({ncs} {current_texts.get('non_consecutive', 'not consecutive')})\n"
            )
        else:
            f.write(
                f"{config['emojis'].get('messages','')} {current_texts['messages'].capitalize()}: {total_msgs_formatted}\n"
            )
            f.write(
                f"{config['emojis'].get('symbols','')} {current_texts.get('symbols', 'symbols').capitalize()}: {total_symbols_formatted}\n"
            )

        f.write(
            f"{config['emojis'].get('avg_symbols','')} {current_texts.get('avg_symbols_in_message', 'Symbols per message')}: {avg_message_length:.0f}\n\n"
        )

        mc = analysis_results['message_counts']
        f.write(f"{config['emojis'].get('pictures','')} {current_texts.get('pictures', 'Pictures')}: {format_number(mc['picture'])}\n")
        f.write(f"{config['emojis'].get('videos','')} {current_texts.get('videos', 'Videos')}: {format_number(mc['video'])}\n")
        f.write(f"{config['emojis'].get('files','')} {current_texts.get('files', 'Files')}: {format_number(mc['file'])}\n")
        f.write(f"{config['emojis'].get('audios','')} {current_texts.get('audios', 'Audios')}: {format_number(mc['audio'])}\n")
        f.write(f"{config['emojis'].get('links','')} {current_texts.get('links', 'Links')}: {format_number(mc['links'])}\n")
        f.write(f"{config['emojis'].get('voice','')} {current_texts.get('voice_messages', 'Voice messages')}: {format_number(mc['voice_message'])}\n")
        f.write(f"{config['emojis'].get('gif','')} GIF: {format_number(mc['gif'])}\n")
        f.write(f"{config['emojis'].get('sticker','')} {current_texts.get('stickers', 'Stickers')}: {format_number(mc['sticker'])}\n")
        f.write(f"{config['emojis'].get('emoji','')} {current_texts.get('emojis', 'Emojis')}: {format_number(mc['emojis'])}\n")
        f.write(f"{config['emojis'].get('poll','')} {current_texts.get('polls', 'Polls')}: {format_number(mc['poll'])}\n")
        f.write(f"{config['emojis'].get('command','')} {current_texts.get('commands', 'Commands')}: {format_number(mc['commands'])}\n")
        f.write(f"{config['emojis'].get('profanity','')} {current_texts.get('profanity_messages', 'Messages with profanity')}: {format_number(mc['profanity'])}\n\n")

        or_word = current_texts.get('or_word', 'or')

        if is_personal_chat:
            # For personal chats, show which user wrote more messages.
            participants = list(analysis_results['user_counts'].keys())
            if len(participants) == 2:
                u_counts = analysis_results['user_counts']
                ncc = analysis_results['non_consecutive_counts']
                user1, user2 = participants
                c1 = u_counts[user1]
                c2 = u_counts[user2]
                nc1 = ncc[user1]
                nc2 = ncc[user2]

                personal_stats_str = current_texts['personal_chat_stats'].format(
                    user1,
                    format_number(c1),
                    format_number(nc1),
                    user2,
                    format_number(c2),
                    format_number(nc2)
                )
                f.write(personal_stats_str + "\n")

                total_symbols = analysis_results['total_symbols']
                # Estimate reading time based on symbol count. 1000 symbols ~ 60 seconds reading time approx.
                total_reading_seconds = (total_symbols / 1000) * 60
                total_reading_minutes = int(total_reading_seconds / 60)
                total_reading_hours = int(total_reading_minutes / 60)
                total_reading_days = total_reading_hours / 24
                days_part = ""
                if total_reading_days >= 1:
                    days_part = current_texts['days'].format(f"{total_reading_days:.2f}")

                reading_time_str = current_texts['reading_time_estimate'].format(
                    int(total_reading_seconds),
                    total_reading_minutes,
                    total_reading_hours,
                    days_part
                )
                f.write("\n" + reading_time_str + "\n")
            else:
                f.write("Unexpected number of participants in personal chat.\n")
        else:
            p_emoji = config['emojis'].get('participant', '')
            top_participants_title = current_texts.get('top_participants', 'Top participants')
            f.write(f"{p_emoji} {top_participants_title}:\n")
            sorted_users = analysis_results['user_counts'].most_common(config.get('top_participants_count'))
            rank = 1
            show_links = config.get('show_user_links', False)
            for user, ucount in sorted_users:
                non_consecutive_count = analysis_results['non_consecutive_counts'][user]
                symbols_val = analysis_results['user_symbols'][user]
                non_consecutive_symbols_val = analysis_results['non_consecutive_symbols'][user]
                user_id = analysis_results['user_ids'].get(user, '')
                if show_non_consecutive:
                    if show_links and user_id:
                        f.write(f"{rank}. {user} (tg://openmessage?user_id={user_id}):\n")
                    else:
                        f.write(f"{rank}. {user}:\n")
                    f.write(
                        f"—— {format_number(ucount)} · {format_number(symbols_val)} {or_word} "
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

            invite_top_text = current_texts['invite_top']
            invite_counts = analysis_results['invite_counts']
            if invite_counts:
                f.write(f"{invite_top_text}:\n")
                sorted_invites = invite_counts.most_common()
                rank = 1
                for inviter, inv_count in sorted_invites:
                    inviter_id = analysis_results['user_ids'].get(inviter, '')
                    if show_links and inviter_id:
                        f.write(
                            f"{rank}. {inviter} (tg://openmessage?user_id={inviter_id}): "
                            f"{format_number(inv_count)} приглашений\n"
                        )
                    else:
                        f.write(f"{rank}. {inviter}: {format_number(inv_count)} приглашений\n")
                    rank += 1
                f.write("\n")

        w_emoji = config['emojis'].get('word', '')
        top_words_text = current_texts.get('top_words', 'Top words')
        f.write(f"{w_emoji} {top_words_text}:\n")
        rank = 1
        for wval, freq in analysis_results['common_words']:
            times_text = current_texts.get('times', 'times')
            f.write(f"{rank}. {wval}: {format_number(freq)} {times_text}\n")
            rank += 1
        f.write("\n")

        ph_emoji = config['emojis'].get('phrase', '')
        top_phrases_text = current_texts.get('top_phrases', 'Top phrases')
        f.write(f"{ph_emoji} {top_phrases_text}:\n")
        rank = 1
        for phrase, freq in analysis_results['common_phrases']:
            times_text = current_texts.get('times', 'times')
            f.write(f"{rank}. {phrase}: {format_number(freq)} {times_text}\n")
            rank += 1
        f.write("\n")

        a_emoji = config['emojis'].get('activity', '')
        activity_text = current_texts.get('activity', 'Activity')
        f.write(f"{a_emoji} {activity_text}:\n")
        activity_data = analysis_results['activity']

        # Activity by hours.
        hours_str = ', '.join([
            f"{config['emojis'].get('list_item', '')} {hour}:00–{hour}:59"
            for hour, _ in activity_data['hours']
        ])
        f.write(hours_str + "\n")

        # Activity by weekdays, localized if possible.
        localized_weekdays = []
        for weekday, _ in activity_data['weekdays']:
            if day_localization and weekday in ru_days:
                idx = ru_days.index(weekday)
                localized_weekdays.append(f"{config['emojis'].get('list_item', '')} {target_days[idx]}")
            else:
                localized_weekdays.append(f"{config['emojis'].get('list_item', '')} {weekday}")
        f.write(', '.join(localized_weekdays) + "\n")

        # Activity by months, localized if possible.
        localized_months = []
        for m, _ in activity_data['months']:
            parts = m.split()
            if month_localization and len(parts) == 2:
                month_ru = parts[0]
                year_str = parts[1]
                if month_ru in ru_months:
                    m_idx = ru_months.index(month_ru)
                    localized_months.append(f"{config['emojis'].get('list_item', '')} {target_months[m_idx].capitalize()} {year_str}")
                else:
                    localized_months.append(f"{config['emojis'].get('list_item', '')} {m}")
            else:
                localized_months.append(f"{config['emojis'].get('list_item', '')} {m}")
        f.write(', '.join(localized_months) + "\n")

        # Activity by years.
        years_str = ', '.join([
            f"{config['emojis'].get('list_item', '')} {year}"
            for year, _ in activity_data['years']
        ])
        f.write(years_str + "\n\n")

        mad_text = current_texts.get('most_active_days', 'Most active days')
        f.write(f"{a_emoji} {mad_text}:\n")
        rank = 1
        ds = analysis_results['date_symbols']
        for date_val, msg_count in analysis_results['top_days']:
            symbol_count = ds[date_val]
            avg_len = symbol_count / msg_count if msg_count else 0
            date_str = date_val.strftime('%d.%m.%Y')
            f.write(
                f"{rank}. {date_str}: ✉️ {format_number(msg_count)}, "
                f"🔣 {format_number(symbol_count)}, 💬 {avg_len:.1f}\n"
            )
            rank += 1
        f.write("\n")

        if analysis_results['creator_name'] and analysis_results['creator_id']:
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
    # Currently only a placeholder. Could be expanded to export structured JSON with stats.
    json_output_data = {}
    with open(json_output_filename, 'w', encoding='utf-8') as jf:
        json.dump(json_output_data, jf, ensure_ascii=False, indent=4)