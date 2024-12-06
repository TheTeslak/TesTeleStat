def configure_in_console(config, current_texts, is_personal_chat):
    # This function allows user-interactive configuration of analysis parameters at runtime.
    # Useful if the user wants to override defaults without editing config.py directly.
    temp_config = {}
    print(current_texts['configuring_settings'])

    time_offset_default = getattr(config, 'time_offset', 0)
    time_offset_prompt = current_texts.get('time_offset_prompt', "Enter time offset in hours (default {default}): ").format(default=time_offset_default)
    time_offset_input = input(time_offset_prompt).strip()
    if time_offset_input:
        try:
            temp_config['time_offset'] = int(time_offset_input)
        except ValueError:
            temp_config['time_offset'] = time_offset_default
    else:
        temp_config['time_offset'] = time_offset_default

    # If personal chat, allow configuring interval for identifying the "first sender" after breaks.
    if is_personal_chat:
        interval_prompt = current_texts.get('first_message_interval_prompt', "After what interval (in hours) to consider who wrote first? (default {default}): ").format(default=getattr(config, 'first_message_interval_hours', 1))
        interval_input = input(interval_prompt).strip()
        if interval_input:
            try:
                temp_config['first_message_interval_hours'] = int(interval_input)
            except ValueError:
                temp_config['first_message_interval_hours'] = getattr(config, 'first_message_interval_hours', 1)
        else:
            temp_config['first_message_interval_hours'] = getattr(config, 'first_message_interval_hours', 1)

        # Option to plot data based on non-consecutive messages in personal chats.
        plot_non_consecutive_default = getattr(config, 'plot_non_consecutive_messages', False)
        plot_non_consecutive_prompt = current_texts.get('plot_non_consecutive_prompt', "Plot based on non-consecutive messages? (y/n, default {default}): ").format(
            default='Yes' if plot_non_consecutive_default else 'No')
        plot_non_consecutive_input = input(plot_non_consecutive_prompt).strip().lower()
        temp_config['plot_non_consecutive_messages'] = plot_non_consecutive_input == 'y' or plot_non_consecutive_input == 'д' or (plot_non_consecutive_input == '' and plot_non_consecutive_default)

    stop_words_default = getattr(config, 'stop_words_type', 'minimal')
    stop_words_options = current_texts.get('stop_words_options', "Choose stop words list (1-minimal, 2-extended, default {default}): ")
    stop_words_prompt = stop_words_options.format(default=stop_words_default)
    stop_words_choice = input(stop_words_prompt).strip()
    if stop_words_choice == '1':
        temp_config['stop_words_type'] = 'minimal'
    elif stop_words_choice == '2':
        temp_config['stop_words_type'] = 'extended'
    else:
        temp_config['stop_words_type'] = stop_words_default

    top_words_count_prompt = current_texts.get('top_words_count_prompt', "Number of top words to display (default {default}): ").format(default=config.top_words_count)
    top_words_count = input(top_words_count_prompt).strip()
    temp_config['top_words_count'] = int(top_words_count) if top_words_count.isdigit() else config.top_words_count

    top_phrases_count_prompt = current_texts.get('top_phrases_count_prompt', "Number of top phrases to display (default {default}): ").format(default=config.top_phrases_count)
    top_phrases_count = input(top_phrases_count_prompt).strip()
    temp_config['top_phrases_count'] = int(top_phrases_count) if top_phrases_count.isdigit() else config.top_phrases_count

    # In group chats, additional configuration:
    if not is_personal_chat:
        exclude_bots_prompt = current_texts.get('exclude_bots_prompt', "Exclude bots? (y/n, default {default}): ").format(default='Yes' if config.exclude_bots else 'No')
        exclude_bots = input(exclude_bots_prompt).strip().lower()
        temp_config['exclude_bots'] = exclude_bots != 'n' and exclude_bots != 'н'

        show_non_consecutive_prompt = current_texts.get('show_non_consecutive_prompt', "Show non-consecutive message counts? (y/n, default {default}): ").format(default='Yes' if config.show_non_consecutive_counts else 'No')
        show_non_consecutive_counts = input(show_non_consecutive_prompt).strip().lower()
        temp_config['show_non_consecutive_counts'] = show_non_consecutive_counts != 'n' and show_non_consecutive_counts != 'н'

        top_participants_count_prompt = current_texts.get('top_participants_count_prompt', "Number of top participants to display (default {default}): ").format(default=config.top_participants_count)
        top_participants_count = input(top_participants_count_prompt).strip()
        temp_config['top_participants_count'] = int(top_participants_count) if top_participants_count.isdigit() else config.top_participants_count

        show_user_links_prompt = current_texts.get('show_user_links_prompt', "Show user links? (y/n, default {default}): ").format(default='Yes' if config.show_user_links else 'No')
        show_user_links = input(show_user_links_prompt).strip().lower()
        temp_config['show_user_links'] = show_user_links != 'n' and show_user_links != 'н'

    # Copy remaining settings from original config.
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
    # Saves the new configuration to confignew.py, allowing the user to persist changed settings.
    with open('confignew.py', 'w', encoding='utf-8') as f:
        for key, value in temp_config.items():
            if isinstance(value, str):
                f.write(f"{key} = '{value}'\n")
            else:
                f.write(f"{key} = {value}\n")
    print("Settings have been saved to confignew.py")