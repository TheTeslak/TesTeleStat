# Name of the main file for analysis. Typically, this would be a Telegram export JSON.
input_file = 'result.json'

# Folder containing JSON files for merging. If '', the current directory is used.
# Useful when the export is split into multiple parts like result1.json, result2.json, etc.
merge_folder = ''

# Output filename pattern: <chat_name> and <timestamp> will be replaced automatically.
output_filename_pattern = '<chat_name>_<timestamp>.txt'

# Choose stop words type: 'minimal' or 'extended'. This affects word frequency analysis.
stop_words_type = 'minimal'

# top_participants_count = None means show all participants. If it's a number, limit to that many.
top_participants_count = None

top_words_count = 100
top_phrases_count = 100

# Emojis to mark sections in the report. These are optional cosmetic enhancements.
emojis = {
    'title': '💬',
    'participant': '👥',
    'word': '🔠',
    'phrase': '📝',
    'activity': '📊',
    'list_item': '➡️',
    'messages': '✉️',
    'symbols': '🔣',
    'avg_symbols': '💬',
    'voice': '🎵',
    'forwarded': '📩',
    'pictures': '🖼',
    'videos': '🎥',
    'gif': '🎬',
    'audios': '🎧',
    'files': '📑',
    'sticker': '💌',
    'command': '❗',
    'emoji': '😊',
    'profanity': '💢',
    'links': '🔗',
    'poll': '📊',
}

# Number of top days to show in "Most active days" section.
top_days_count = 10

# Whether to display non-consecutive message counts (counts where user changed, resetting the chain).
show_non_consecutive_counts = True

# Whether to exclude bots from analysis. Useful if you don't want bot messages skewing stats.
exclude_bots = True
bot_identifiers = ['Bot']

# Day and month names for different locales. The analyzer will choose the array based on selected language.
day_names = {
    'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
    'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
}
month_names = {
    'ru': ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
}

# Commands often start with '/', like Telegram bot commands. Adjust if needed.
commands_identifiers = ['/']

import re
emoji_pattern = re.compile("[" 
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U0001F900-\U0001F9FF"
                           u"\U0001FA70-\U0001FAFF"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

url_pattern = re.compile(
    r'(?i)\b((?:https?:\/\/|www\d{0,3}[.]|telegram[.]me\/|t[.]me\/|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+)',
    re.IGNORECASE)

# If True, author links (GitHub, Telegram channel) will be shown at the end of the report.
show_author_links = True

# If True, links to user profiles are shown for participants (tg://openmessage?user_id=...).
show_user_links = False

# After this interval (in hours), the personal chat "first sender" calculation resets.
first_message_interval_hours = 1

# Directory containing word lists such as stop words or profanity words.
words_dir = 'words'

# Time offset in hours to adjust timestamps if your data is in a different timezone than desired.
time_offset = 0

# If True, when plotting personal chat data, non-consecutive messages are used instead of total counts.
plot_non_consecutive_messages = False