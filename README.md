# Mitigating Unbounded Data Growth in Chat Systems

This project presents a practical and lightweight pipeline for managing large volumes of real-time conversational data using a combination of deduplication, tiered retention, compression, and summarization. The approach aims to **control storage overhead**, **maintain data usability**, and **support basic log analytics** — all in a modular, efficient Python-based system.

---

## 📌 Overview

Modern systems that handle high-frequency text data (like chatbots, support logs, or telemetry) often suffer from **unbounded data growth**, leading to storage issues and performance bottlenecks. This project demonstrates a solution using:

- Real-time ingestion and deduplication  
- Tiered log retention: **Hot → Warm → Cold**  
- Gzip-based compression for long-term storage  
- Message activity summarization and visualization  
- Compression analytics (ratio, time, file size)

> Dataset used: [Ubuntu Dialogue Corpus](https://github.com/rkadlec/ubuntu-ranking-dataset-creator)

---

## Features:-

- **Tiered Storage**: Inspired by real-world log management systems, data is progressively aged from hot (active) to warm (intermediate) to cold (archived) storage.
- **Deduplication**: Exact-message deduplication at ingestion avoids unnecessary storage of repeated user messages.
- **Compression**: Cold logs are compressed with gzip, with detailed logging of size reduction and time taken.
- **Summarization**: Hourly summaries are generated to support monitoring and analysis without scanning raw logs.
- **Visualizations**: Includes bar charts and time-series plots for message trends and activity distribution.

---

## 📁 Project Structure
```
├── main.py # Entry point: runs the streaming + retention + summarization pipeline
├── utils.py # Utility functions: file ops, compression, timestamp parsing
├── summarize.py # Aggregates hourly message counts for summarization
├── visualize.py # Generates graphs (bar charts, line plots)
├── summaries/
│ ├── hourly_summary.csv # Auto-generated CSV of hourly message counts
│ └── message_volume.png # Output visualizations
├── hot_chat_logs/ # Recently ingested logs
├── warm_chat_logs/ # Intermediate storage
├── cold_chat_archives/ # Cold logs awaiting compression
├── compressed_logs/ # Compressed gzip archives and compression log
│ └── compression_log.csv # Logged stats: sizes, ratios, time
└── Ubuntu-dialogue-corpus/ # Contains input CSV files
```



