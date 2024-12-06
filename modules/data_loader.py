import json
import os
import re
import ijson

def load_json_file_streaming(input_file, header_only=False):
    # Streams through the file to find basic header info without loading full content.
    # If header_only=True, stop after reading name, type, and id.
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            parser = ijson.parse(f)
            data = {}
            current_key = None
            for prefix, event, value in parser:
                if prefix == '' and event == 'map_key':
                    current_key = value
                elif current_key == 'name' and prefix == 'name' and event == 'string':
                    data['name'] = value
                elif current_key == 'type' and prefix == 'type' and event == 'string':
                    data['type'] = value
                elif current_key == 'id' and prefix == 'id' and event in ('number', 'string'):
                    data['id'] = value
                elif current_key == 'messages' and event == 'start_array':
                    if header_only:
                        # If we only need headers, stop here before reading messages.
                        break
                    else:
                        # If we need full data, read messages in a streaming manner.
                        data['messages'] = []
                        for msg in ijson.items(f, 'messages.item'):
                            data['messages'].append(msg)
                    break
            return data
    except:
        # If the file is invalid or any error occurs, return None to signal invalid JSON.
        return None

def merge_json_files(folder_path, output_file, current_texts):
    # Merges multiple JSON files (like result1.json, result2.json...) into one combined file.
    # Useful if the chat export is split into segments.
    merged_messages = {}
    pattern = re.compile(r'^result\d*\.json$')
    header_data = None
    if not os.path.isdir(folder_path) or folder_path == '':
        # If no folder is specified, use current directory.
        folder_path = '.'

    files_found = False
    for filename in os.listdir(folder_path):
        if pattern.match(filename):
            files_found = True
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"Processing file: {file_path}")
                data = load_json_file_streaming(file_path)
                if data:
                    if header_data is None:
                        # Use header from the first found file.
                        header_data = {k: data[k] for k in data if k != 'messages'}
                    for message in data.get('messages', []):
                        message_id = message.get('id')
                        if message_id is not None:
                            merged_messages[message_id] = message
    if not files_found:
        print("No files matching 'result*.json' pattern found in '.'")
        return False

    if not merged_messages:
        print("No messages found to merge.")
        return False

    # Sort messages by id to maintain chronological order (assuming id correlates to chronology).
    sorted_messages = sorted(merged_messages.values(), key=lambda x: x.get('id'))

    if header_data:
        header_data['messages'] = sorted_messages
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(header_data, f, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing merged file: {e}")
            return False
    else:
        print("No header data found. Cannot save merged file.")
        return False