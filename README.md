# Teslak Telegram Statistic Analyzer

![Version](https://img.shields.io/badge/Version-1.3-brightgreen.svg) ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![JSON](https://img.shields.io/badge/JSON-Compatible-orange.svg)

## 📚 Navigation / Навигация
- [Teslak Telegram Statistic Analyzer](#teslak-telegram-statistic-analyzer)
  - [📚 Navigation / Навигация](#-navigation--навигация)
  - [English](#english)
    - [📋 Features](#-features)
    - [⚙️ Usage](#️-usage)
    - [🔧 Configuration](#-configuration)
    - [📄 Examples](#-examples)
      - [Channel Analysis (Sample)](#channel-analysis-sample)
      - [Group Chat Analysis (Sample)](#group-chat-analysis-sample)
  - [Русский](#русский)
    - [📋 Возможности](#-возможности)
    - [⚙️ Использование](#️-использование)
    - [🔧 Конфигурация](#-конфигурация)
    - [📄 Примеры](#-примеры)
      - [Анализ канала (Пример)](#анализ-канала-пример)
      - [Анализ чата (Пример)](#анализ-чата-пример)

---

## English

### 📋 Features
- Analyze both group chats and channels
- Count messages, characters, links, reactions, authors, and profanity
- Display top words, phrases, participants, and posts by reactions
- Generate visual activity graphs
- Merge JSON files without duplicates
- Customize settings in `config.py`
- Supports multiple languages
- Counts each link in a message separately (unlike Telegram)

### ⚙️ Usage

1. **Prepare Export**
   - Export your chat or channel in JSON format
   - Place `result.json` in the script folder
   - For multiple files: name them `result1.json`, `result2.json`, etc.

2. **Run Script**
   - Open a terminal in the script folder
   - Install dependencies: `pip install -r requirements.txt`
   - Execute: `python start.py`

3. **Follow Instructions**
   - Select an action
   - Adjust parameters if needed

4. **View Results**
   - Reports are saved as TXT, PNG, or JSON

### 🔧 Configuration
Edit `config.py` to customize:
- **Input/Output**: Specify files and merging options
- **Analysis Parameters**: Set top participants, words, phrases, days, and reactions
- **Exclude Bots**: Remove bots from counts
- **Time Offset**: Adjust for different time zones
- **Language and Emojis**: Select preferred language and emoji settings

### 📄 Examples

#### Channel Analysis (Sample)
```
Channel statistics "Example Channel" 01.01.2024 – 31.12.2024

Name: Example Channel
Type: public_channel

✉️ Messages: 10,000
🔣 Characters: 45,000
💬 Average characters per message: 4.5

🖼 Images: 7,200
🎥 Videos: 600
📑 Files: 10
🎧 Audios: 5
🔗 Links: 50
🎵 Voice messages: 15
🎬 GIFs: 20
💌 Stickers: 25
😊 Emojis: 50
📊 Polls: 5
❗ Commands: 10
💢 Profanity: 100

👥 Authors by number of posts:
1. Author1: 3,500
2. Author2: 2,000
3. Author3: 1,500

📊 Reactions:
1. 👍: 6,872
2. 💘: 3,526
3. ❤: 3,202

📊 Activity:
➡️ Most active time: 15:00–16:59
➡️ Most active day: Monday
➡️ Most active month: July 2024

📊 Most active days:
1. 21.03.2024: ✉️ 402, 🔣 5,808, 💬 14.4
2. 22.03.2024: ✉️ 166, 🔣 962, 💬 5.8
3. 31.03.2024: ✉️ 138, 🔣 32, 💬 0.2
4. 23.03.2024: ✉️ 93, 🔣 294, 💬 3.2
5. 31.05.2024: ✉️ 89, 🔣 1,045, 💬 11.7
```

#### Group Chat Analysis (Sample)
```
Chat statistics "Example Group Chat" 01.06.2024 – 30.06.2024

✉️ Messages: 250
🔣 Characters: 12,500
💬 Average characters per message: 50

🖼 Images: 50
🎥 Videos: 10
📑 Files: 5
🎧 Audios: 2
🔗 Links: 30
🎵 Voice messages: 20
🎬 GIFs: 5
💌 Stickers: 8
😊 Emojis: 10
📊 Polls: 1
❗ Commands: 2
💢 Profanity: 5

👥 Top participants:
1. User1: 150 messages
2. User2: 80 messages
3. User3: 20 messages

📊 Activity:
➡️ Most active time: 18:00–20:59
➡️ Most active day: Friday
➡️ Most active month: June 2024

📊 Most active days:
1. 05.06.2024: ✉️ 19, 🔣 33, 💬 1.7
2. 30.09.2024: ✉️ 17, 🔣 401, 💬 23.6
3. 01.10.2024: ✉️ 9, 🔣 3,631, 💬 403.4
4. 18.12.2024: ✉️ 4, 🔣 1,311, 💬 327.8
5. 17.12.2024: ✉️ 1, 🔣 1, 💬 1.0
```

Contributions and feedback are welcome.

---

## Русский

### 📋 Возможности
- Анализ групповых чатов и каналов
- Подсчёт сообщений, символов, ссылок, реакций, авторов и нецензурной лексики
- Отображение топ-слов, фраз, участников и постов по реакциям
- Построение графиков активности
- Объединение JSON-файлов без дубликатов
- Настройка через `config.py`
- Поддержка нескольких языков
- Подсчёт каждой ссылки в сообщении отдельно (в отличие от Telegram)

### ⚙️ Использование

1. **Подготовка экспорта**
   - Экспортируйте чат или канал в формате JSON
   - Поместите `result.json` в папку со скриптом
   - Для нескольких файлов: используйте имена `result1.json`, `result2.json` и т.д.

2. **Запуск**
   - Откройте терминал в папке со скриптом
   - Установите зависимости: `pip install -r requirements.txt`
   - Выполните: `python start.py`

3. **Следуйте инструкциям**
   - Выберите действие
   - Настройте параметры при необходимости

4. **Просмотр результатов**
   - Отчёты сохраняются в формате TXT, PNG или JSON

### 🔧 Конфигурация
Настройте `config.py`:
- **Вход/выход**: Укажите файлы и параметры слияния
- **Параметры анализа**: Задайте топ участников, слов, фраз, дней и реакций
- **Исключение ботов**: Удалите ботов из подсчётов
- **Часовой пояс**: Настройте для разных часовых зон
- **Язык и эмодзи**: Выберите предпочитаемый язык и настройки эмодзи

### 📄 Примеры

#### Анализ канала (Пример)
```
Статистика канала "Пример Канала" 01.01.2024 – 31.12.2024

Название: Пример Канала
Тип: public_channel

✉️ Сообщений: 10,000
🔣 Символов: 45,000
💬 Среднее символов в сообщении: 4.5

🖼 Изображений: 7,200
🎥 Видео: 600
📑 Файлы: 10
🎧 Аудио: 5
🔗 Ссылки: 50
🎵 Голосовые: 15
🎬 GIF: 20
💌 Стикеры: 25
😊 Эмодзи: 50
📊 Опросы: 5
❗ Команды: 10
💢 Нецензурщина: 100

👥 Авторы по количеству постов:
1. Автор1: 3,500
2. Автор2: 2,000
3. Автор3: 1,500

📊 Реакции:
1. 👍: 6,872
2. 💘: 3,526
3. ❤: 3,202

📊 Активность:
➡️ Самое активное время: 15:00–16:59
➡️ Самый активный день: Понедельник
➡️ Самый активный месяц: Июль 2024

📊 Самые активные дни:
1. 21.03.2024: ✉️ 402, 🔣 5,808, 💬 14.4
2. 22.03.2024: ✉️ 166, 🔣 962, 💬 5.8
3. 31.03.2024: ✉️ 138, 🔣 32, 💬 0.2
4. 23.03.2024: ✉️ 93, 🔣 294, 💬 3.2
5. 31.05.2024: ✉️ 89, 🔣 1,045, 💬 11.7
```

#### Анализ чата (Пример)
```
Статистика чата "Пример Чата" 01.06.2024 – 30.06.2024

✉️ Сообщений: 250
🔣 Символов: 12,500
💬 Среднее символов/сообщение: 50

🖼 Изображений: 50
🎥 Видео: 10
📑 Файлы: 5
🎧 Аудио: 2
🔗 Ссылки: 30
🎵 Голосовые: 20
🎬 GIF: 5
💌 Стикеры: 8
😊 Эмодзи: 10
📊 Опросы: 1
❗ Команды: 2
💢 Нецензурщина: 5

👥 Топ участников:
1. Пользователь1: 150 сообщений
2. Пользователь2: 80 сообщений
3. Пользователь3: 20 сообщений

📊 Активность:
➡️ Самое активное время: 18:00–20:59
➡️ Самый активный день: Пятница
➡️ Самый активный месяц: Июнь 2024

📊 Самые активные дни:
1. 05.06.2024: ✉️ 19, 🔣 33, 💬 1.7
2. 30.09.2024: ✉️ 17, 🔣 401, 💬 23.6
3. 01.10.2024: ✉️ 9, 🔣 3,631, 💬 403.4
4. 18.12.2024: ✉️ 4, 🔣 1,311, 💬 327.8
5. 17.12.2024: ✉️ 1, 🔣 1, 💬 1.0
```

Приветствуются идеи и улучшения.