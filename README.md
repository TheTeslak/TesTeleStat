# Telegram Chat Analysis

![Version](https://img.shields.io/badge/Version-1.2-brightgreen.svg) ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![JSON](https://img.shields.io/badge/JSON-Compatible-orange.svg)  

## 📚 Navigation / Навигация
- [English](#english)
  - [Features](#features)
  - [Usage](#usage)
  - [Configuration](#configuration)
- [Русский](#русский)
  - [Возможности](#возможности)
  - [Использование](#использование)
  - [Конфигурация](#конфигурация)

---

## English

### 📋 Features
- **Local Processing**
- **Activity Graphs**: Generate graphs showing activity
- **JSON Merging**: Merges overlapping files without duplication
- **Detailed Statistics**: Includes message count, word frequency, participant rankings, etc.
- **Customizable**: Configure stop-words and other settings in `config.py`
- **Multilingual Support**

### ⚙️ Usage

1. **Prepare the Export**
   - Export your Telegram chat **in JSON format**
   - Place the `result.json` file in the script directory
   - Optionally, for merging multiple files, name them `result1.json`, `result2.json`, and so on.

2. **Run the Script**
   - Open a terminal in the script directory
   - Install dependencies: `pip install -r requirements.txt`
   - Run the script: `python start.py`

3. **Follow the Interface**
   - Select an action
   - Adjust parameters if needed, or use the default values

4. **View the Results**
   - Reports will be saved in TXT, PNG, and optionally JSON formats

#### Sample Report:
```
Chat statistics for "Chat Name" over the period: X – Y

✉️ Messages: [total] ([unique])
🔣 Characters: [total] ([unique])
💬 Avg. characters per message: [average]

🖼 Images: [count]
📹 Videos: [count]
...
```

### 🔧 Configuration
Customize the analysis by editing `config.py`:
- **Input/Output Settings**: Specify input files, merge directories, and output file names
- **Analysis Parameters**: Set the number of top participants, words, phrases, and active days
- **Exclude Bots**: Remove bots from message counts
- **Time Shift**: Adjust for timezone differences
- **Language and Emojis**


Feel free to contribute by reporting ideas, bugs, or solutions.

---
## Русский

### 📋 Возможности
- **Локальная обработка**
- **Начертание графиков активности**
- **Объединение JSON**: пересекающиеся файлы объединяются без дублирования
- **Детальная статистика**: количество сообщений, частота слов, рейтинг участников, etc
- **Настраиваемость**: стоп-слова и другое в `config.py`
- **Мультиязычность**

### ⚙️ Использование

1. **Подготовьте экспорт**
   - Экспортируйте чат Telegram **в формате JSON**
   - Поместите файл `result.json` в директорию со скриптом
   - Опционально для объединения нескольких файлов назвать их `result1.json`, `result2.json` и т.д.

2. **Запуск скрипта**
   - Откройте терминал в директории со скриптом
   - Установите зависимости: `pip install -r requirements.txt`
   - Выполните: `python start.py`

3. **Следуйте интерфейсу**
   - Выберите действие
   - Настройте параметры при необходимости или используйте значения по умолчанию

4. **Просмотр результатов**
   - Отчёты будут сохранены в формате TXT, PNG, и, опционально, JSON

#### Пример отчёта:
```
Статистика чата "Название чата" за период: X – Y

✉️ Сообщений: [всего] ([не подряд])
🔣 Символов: [всего] ([не подряд])
💬 Символов в сообщении: [среднее]

🖼 Изображений: [количество]
📹 Видео: [количество]
...
```

### 🔧 Конфигурация
Настройте анализ, отредактировав `config.py`:
- **Настройки входа/выхода**: укажите входные файлы, папки для объединения и имена выходных файлов
- **Параметры анализа**: задайте количество топ-участников, слов, фраз и активных дней
- **Исключение ботов из подсчёта**
- **Часовой сдвиг**: корректировка разницы в часовых поясах
- **Язык и эмодзи**


Участвуйте в улучшении: сообщайте об идеях, багах и решениях.