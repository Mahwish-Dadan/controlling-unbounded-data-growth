import os
import json
import shutil
import gzip
from datetime import datetime, timedelta


def ensure_dirs():
    for folder in ['hot_chat_logs', 'warm_chat_logs', 'cold_chat_archives', 'compressed_logs', 'summaries']:
        os.makedirs(folder, exist_ok=True)


def write_json_to_folder(folder, data, fname=None):
    if not fname:
        fname = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.json"
    path = os.path.join(folder, fname)
    with open(path, 'w') as f:
        json.dump(data, f)
    return path


def compress_file(src_path, dest_folder):
    import time
    import csv

    # Create destination path
    compressed_path = os.path.join(dest_folder, os.path.basename(src_path) + '.gz')

    # Timing compression
    start_time = time.time()
    with open(src_path, 'rb') as f_in:
        with gzip.open(compressed_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    end_time = time.time()

    # Get sizes
    original_size = os.path.getsize(src_path)
    compressed_size = os.path.getsize(compressed_path)
    compression_time = round(end_time - start_time, 4)
    compression_ratio = round(original_size / compressed_size, 2) if compressed_size > 0 else 0

    # Remove original file
    os.remove(src_path)

    # Log to CSV
    log_file = os.path.join(dest_folder, 'compression_log.csv')
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Original File', 'Compressed File', 'Original Size (bytes)',
                             'Compressed Size (bytes)', 'Compression Ratio', 'Time (s)'])
        writer.writerow([
            datetime.utcnow().isoformat(),
            os.path.basename(src_path),
            os.path.basename(compressed_path),
            original_size,
            compressed_size,
            compression_ratio,
            compression_time
        ])


def move_file(src, dest_folder):
    shutil.move(src, os.path.join(dest_folder, os.path.basename(src)))


def parse_time_str(t):
    return datetime.utcnow()
