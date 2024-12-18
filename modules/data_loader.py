import json
import os
import re
import ijson

def load_json_file_streaming(input_file, header_only=False):
    # Streams through JSON to find header info and possibly messages.
    # If header_only=True, stop after reading basic info without loading messages.
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
                        break
                    else:
                        data['messages'] = []
                        for msg in ijson.items(f, 'messages.item'):
                            data['messages'].append(msg)
                    break
            return data
    except:
        return None

def merge_json_files(folder_path, output_file, current_texts):
    # Merges multiple resultX.json files into one, preserving message order.
    merged_messages = {}
    pattern = re.compile(r'^result\d*\.json$')
    header_data = None
    if not os.path.isdir(folder_path) or folder_path == '':
        folder_path = '.'

    files_found = False
    for filename in os.listdir(folder_path):
        if pattern.match(filename):
            files_found = True
            file_path = os.path.join(folder_path, filename)
            print(current_texts['processing_file'].format(file_path))
            data = load_json_file_streaming(file_path)
            if data:
                if header_data is None:
                    header_data = {k: data[k] for k in data if k != 'messages'}
                for message in data.get('messages', []):
                    message_id = message.get('id')
                    if message_id is not None:
                        merged_messages[message_id] = message
    if not files_found:
        print(current_texts['no_files_found_pattern'])
        return False

    if not merged_messages:
        print(current_texts['no_messages_found_merge'])
        return False

    sorted_messages = sorted(merged_messages.values(), key=lambda x: x.get('id'))
    if header_data:
        header_data['messages'] = sorted_messages
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(header_data, f, ensure_ascii=False)
            return True
        except Exception as e:
            print(current_texts['error_writing_merged_file'].format(e))
            return False
    else:
        print(current_texts['no_header_data_merge'])
        return False