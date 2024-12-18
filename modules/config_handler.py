def configure_in_console(config, current_texts, is_personal_chat):
    print(current_texts['configuring_settings'])
    time_offset_default = getattr(config, 'time_offset', 0)
    time_offset_prompt = current_texts['time_offset_prompt'].format(default=time_offset_default)
    time_offset_input = input(time_offset_prompt).strip()
    if time_offset_input:
        try:
            temp_time_offset = int(time_offset_input)
        except ValueError:
            temp_time_offset = time_offset_default
    else:
        temp_time_offset = time_offset_default

    temp_config = {}
    temp_config['time_offset'] = temp_time_offset

    if is_personal_chat:
        interval_prompt = current_texts['first_message_interval_prompt'].format(default=getattr(config, 'first_message_interval_hours', 1))
        interval_input = input(interval_prompt).strip()
        if interval_input:
            try:
                temp_config['first_message_interval_hours'] = int(interval_input)
            except ValueError:
                temp_config['first_message_interval_hours'] = getattr(config, 'first_message_interval_hours', 1)
        else:
            temp_config['first_message_interval_hours'] = getattr(config, 'first_message_interval_hours', 1)

        plot_non_consecutive_default = getattr(config, 'plot_non_consecutive_messages', False)
        pnc_def_str = 'Yes' if plot_non_consecutive_default else 'No'
        plot_non_consecutive_prompt = current_texts['plot_non_consecutive_prompt'].format(default=pnc_def_str)
        plot_non_consecutive_input = input(plot_non_consecutive_prompt).strip().lower()
        temp_config['plot_non_consecutive_messages'] = plot_non_consecutive_input in ('y', 'д') or (plot_non_consecutive_input == '' and plot_non_consecutive_default)

    stop_words_default = getattr(config, 'stop_words_type', 'minimal')
    swo_prompt = current_texts['stop_words_options'].format(default=stop_words_default)
    stop_words_choice = input(swo_prompt).strip()
    if stop_words_choice == '1':
        temp_config['stop_words_type'] = 'minimal'
    elif stop_words_choice == '2':
        temp_config['stop_words_type'] = 'extended'
    else:
        temp_config['stop_words_type'] = stop_words_default

    tw_prompt = current_texts['top_words_count_prompt'].format(default=config.top_words_count)
    top_words_count = input(tw_prompt).strip()
    temp_config['top_words_count'] = int(top_words_count) if top_words_count.isdigit() else config.top_words_count

    tp_prompt = current_texts['top_phrases_count_prompt'].format(default=config.top_phrases_count)
    top_phrases_count = input(tp_prompt).strip()
    temp_config['top_phrases_count'] = int(top_phrases_count) if top_phrases_count.isdigit() else config.top_phrases_count

    if not is_personal_chat:
        eb_prompt = current_texts['exclude_bots_prompt'].format(default='Yes' if config.exclude_bots else 'No')
        exclude_bots = input(eb_prompt).strip().lower()
        temp_config['exclude_bots'] = exclude_bots not in ('n', 'н')

        snc_prompt = current_texts['show_non_consecutive_prompt'].format(default='Yes' if config.show_non_consecutive_counts else 'No')
        show_non_consecutive_counts = input(snc_prompt).strip().lower()
        temp_config['show_non_consecutive_counts'] = show_non_consecutive_counts not in ('n', 'н')

        tpc_prompt = current_texts['top_participants_count_prompt'].format(default=config.top_participants_count)
        top_participants_count = input(tpc_prompt).strip()
        temp_config['top_participants_count'] = int(top_participants_count) if top_participants_count.isdigit() else config.top_participants_count

        sul_prompt = current_texts['show_user_links_prompt'].format(default='Yes' if config.show_user_links else 'No')
        show_user_links = input(sul_prompt).strip().lower()
        temp_config['show_user_links'] = show_user_links not in ('n', 'н')

    temp_config['input_file'] = config.input_file
    temp_config['merge_folder'] = config.merge_folder
    temp_config['output_filename_pattern'] = config.output_filename_pattern
    temp_config['show_author_links'] = config.show_author_links
    temp_config['commands_identifiers'] = config.commands_identifiers
    temp_config['emoji_pattern'] = config.emoji_pattern
    temp_config['url_pattern'] = config.url_pattern
    temp_config['day_names'] = config.day_names
    temp_config['month_names'] = config.month_names
    temp_config['top_days_count'] = config.top_days_count
    temp_config['bot_identifiers'] = config.bot_identifiers
    temp_config['emojis'] = config.emojis
    temp_config['words_dir'] = config.words_dir

    return temp_config

def save_config_to_file(temp_config):
    with open('confignew.py', 'w', encoding='utf-8') as f:
        for key, value in temp_config.items():
            if isinstance(value, str):
                f.write(f"{key} = '{value}'\n")
            else:
                f.write(f"{key} = {value}\n")
    print("Settings have been saved to confignew.py")