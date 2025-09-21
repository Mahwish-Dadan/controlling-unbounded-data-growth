import os
import csv
import json
import time
from datetime import datetime, timedelta
from utils import ensure_dirs, write_json_to_folder, move_file, compress_file, parse_time_str
from summarize import summarize_logs

# CONFIGURATIONS
CSV_FILES = ['Ubuntu-dialogue-corpus/dialogueText.csv']
HOT_RETENTION_MIN = 0.1
WARM_RETENTION_MIN = 0.2
COLD_RETENTION_MIN = 0.5
DEDUP_CACHE = set()
MAX_MESSAGES = 800


def stream_from_csv():
    for file in CSV_FILES:
        with open(file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield {
                    "timestamp": row.get('date'),
                    "from": row.get('from'),
                    "to": row.get('to'),
                    "text": row.get('text'),
                    "dialogueID": row.get('dialogueID')
                }


def is_duplicate(msg):
    key = (msg['from'], msg['text'])
    if key in DEDUP_CACHE:
        return True
    DEDUP_CACHE.add(key)
    return False


def move_old_files(src_folder, dest_folder, older_than_minutes):
    now = datetime.utcnow()
    for fname in os.listdir(src_folder):
        path = os.path.join(src_folder, fname)
        if not fname.endswith('.json'):
            continue
        with open(path) as f:
            try:
                data = json.load(f)
                t = parse_time_str(data.get('timestamp'))
                if now - t > timedelta(minutes=older_than_minutes):
                    move_file(path, dest_folder)
            except:
                continue

def compress_old_cold_files():
    for fname in os.listdir('cold_chat_archives'):
        if not fname.endswith('.json'):
            continue
        path = os.path.join('cold_chat_archives', fname)
        compress_file(path, 'compressed_logs')


def main():
    ensure_dirs()
    print("Starting ingestion...")

    stream = stream_from_csv()
    start_time = time.time()
    message_count = 0

    for msg in stream:
        if is_duplicate(msg):
            continue

        write_json_to_folder('hot_chat_logs', msg)
        message_count += 1

        # If max limit is reached
        if message_count >= MAX_MESSAGES:
            print(f"Reached {MAX_MESSAGES} messages. Stopping ingestion.")
            break

        # Trigger aging and compression every 60 seconds
        if time.time() - start_time > 60:
            print("Running retention and summarization...")
            move_old_files('hot_chat_logs', 'warm_chat_logs', HOT_RETENTION_MIN)
            move_old_files('warm_chat_logs', 'cold_chat_archives', WARM_RETENTION_MIN)
            compress_old_cold_files()
            summarize_logs('hot_chat_logs')
            start_time = time.time()

        time.sleep(0.1)  # Simulate slow streaming

    # ⚠️ Force retention & compression before exit
    print("Final retention and compression run before exit...")
    move_old_files('hot_chat_logs', 'warm_chat_logs', HOT_RETENTION_MIN)
    move_old_files('warm_chat_logs', 'cold_chat_archives', WARM_RETENTION_MIN)
    compress_old_cold_files()
    summarize_logs('hot_chat_logs')


if __name__ == "__main__":
    main()
