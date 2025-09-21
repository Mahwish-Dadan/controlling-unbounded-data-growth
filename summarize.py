import os
import json
import csv
from collections import defaultdict
from datetime import datetime

def summarize_logs(input_folder, output_csv='summaries/hourly_summary.csv'):
    hour_counts = defaultdict(int)
    user_counts = defaultdict(int)

    for fname in os.listdir(input_folder):
        if not fname.endswith('.json'):
            continue
        with open(os.path.join(input_folder, fname)) as f:
            data = json.load(f)
            timestamp = data.get('date') or data.get('timestamp')
            hour = timestamp[:13] if timestamp else 'unknown'
            user = data.get('from', 'unknown')
            hour_counts[hour] += 1
            user_counts[user] += 1

    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Hour', 'Messages'])
        for hour, count in sorted(hour_counts.items()):
            writer.writerow([hour, count])
