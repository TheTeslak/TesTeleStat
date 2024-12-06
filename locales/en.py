texts = {
    'non_consecutive': "not consecutive",
    'or_word': "or",
    'messages': "messages",
    'symbols': "symbols",
    'pictures': "Pictures",
    'videos': "Videos",
    'audios': "Audios",
    'files': "Files",
    'stickers': "Stickers",
    'commands': "Commands",
    'emojis': "Emojis",
    'profanity_messages': "Profanity",
    'polls': "Polls",
    'links': "Links",
    'top_participants': "Top participants",
    'top_words': "Top words",
    'top_phrases': "Top phrases",
    'times': "times",
    'activity': "Activity",
    'most_active_days': "Most active days",
    'average_message_length': "average message length",
    'voice_messages': "Voice messages",
    'forwards': "Forwards",

    'date_range_for': "for the period",
    'reading_time_estimate': "To read the entire conversation, you will need approximately {0} seconds. This is {1} minutes or {2} hours{3}.",
    'includes_media': "Including media files: {0}",
    'hours': "hours",
    'days': " or {0} days",
    'creator_info': "Group creator: {0}, ID: {1}",

    'day_names': {
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    },
    'month_names': {
        'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    },

    'first_sender_triangle_label': "First Sender After Interval",
    'date_label': "Date",
    'message_count_label': "Number of Messages",
    'chat_activity_in_year': "Chat Activity in {0}",
    'group_chat_activity_in_year': "Group Chat Activity in {0}",

    'total_messages': "Total messages in chat: {0}",
    'date_range': "",
    'personal_chat_stats': "{0} wrote more: {1} ({2} not consecutive) messages\n{3}: {4} ({5} not consecutive) messages",
    'communication_graph_saved': "Communication graph saved to '{0}'.",

    'ascii_art': "\033[32m" + r"""
  _______         _____ _           _    _____ _        _
 |__   __|       / ____| |         | |  / ____| |      | |
    | | ___  ___| |    | |__   __ _| |_| (___ | |_ __ _| |_
    | |/ _ \/ __| |    | '_ \ / _` | __|\___ \| __/ _` | __|
    | |  __/\__ \ |____| | | | (_| | |_ ____) | || (_| | |_
    |_|\___||___/\_____|_| |_|\__,_|\__|_____/ \__\__,_|\__|
""" + "\033[0m",
    'description': "Telegram chat statistics based on JSON export",

    'menu_options': {
        '0': "Сменить язык",
        '1': "Analyze file",
        '2': "Analyze and save results to TXT and JSON files",
        '3': "Merge resultNUMBER.json files and save to file",
    },

    'prompt_choice': "Enter your choice number and press Enter (default is 1): ",
    'start_analysis': "Starting analysis...",
    'start_analysis_save': "Starting analysis and saving to text and JSON files...",
    'file_not_found': "❌ File '{0}' not found.",
    'file_size_warning': "⚠️ File size is {0} MB, processing may take some time.",
    'file_size_large_warning': "⚠️ File size is {0} GB, processing may take a very long time on weak devices and may be unstable.",
    'invalid_json': "Error: Invalid JSON file format.",
    'no_messages': "The file contains no messages for analysis.",
    'processing_completed': "✅ Analysis completed in {0:.2f} seconds. Results saved to '{1}'.",
    'unprocessed_messages': "Failed to process {0:.2f}% of messages.",
    'error_count': "Number of errors: {0}. Details in '{1}'.",
    'author_links': "⚡️ GitHub (check updates): {0}\n⚡️ Telegram channel: {1}",
    'select_action': "Select an action:",
    'processing': "Processed {0} messages... {1}",
    'press_enter_to_return': "Press Enter to return to the main menu...",
    'title_changes': "Title changes: {0}",
    'invite_top': "Top users by invitations",
    'config_prompt': "1. Use standard settings from config.py\n2. Configure in console\nEnter your choice number and press Enter (default is 1): ",
    'save_config_prompt': "Save these settings to confignew.py? (y/n, default n): ",
    'first_message_interval_prompt': "After what interval (in hours) to consider who wrote first? (default {default}): ",
    'configuring_settings': "Configuring settings:",
    'time_offset_prompt': "Enter time offset in hours (default {default}): ",
    'stop_words_options': "Choose stop words list (1-minimal, 2-extended, default {default}): ",
    'top_words_count_prompt': "Number of top words to display (default {default}): ",
    'top_phrases_count_prompt': "Number of top phrases to display (default {default}): ",
    'exclude_bots_prompt': "Exclude bots? (y/n, default {default}): ",
    'show_non_consecutive_prompt': "Show non-consecutive message counts? (y/n, default {default}): ",
    'top_participants_count_prompt': "Number of top participants to display (default {default}): ",
    'show_user_links_prompt': "Show user links? (y/n, default {default}): ",
    'plot_non_consecutive_prompt': "Plot based on non-consecutive messages? (y/n, default {default}): ",
    'date_range_prompt': "Enter date range in format 'DD.MM.YYYY-DD.MM.YYYY' or leave empty for all time: ",
    'invalid_date_range': "❌ Invalid date range format.",
    'no_messages_in_range': "No messages found in the specified date range.",
}