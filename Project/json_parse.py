import json
import psycopg2
from pathlib import Path
from datetime import datetime

# Directory containing subfolders like BA, META, etc.
json_dir = Path('./newsData/')

# Rename any files with no extension to .json
for subdir in json_dir.iterdir():
    if subdir.is_dir():
        for file in subdir.iterdir():
            if file.is_file() and not file.suffix:
                new_file = file.with_name(file.name + '.json')
                file.rename(new_file)
                print(f"✅ Renamed {file.name} -> {new_file.name}")

# Find all .json files
json_files = sorted(json_dir.rglob("*.json"))

if not json_files:
    print("⚠️ No JSON files found.")
else:
    print(f"🗂 Found {len(json_files)} JSON files to import.")

# PostgreSQL connection settings
db_config = {
    "host": "localhost",
    "user": "postgres",
    "password": "csci126",
    "dbname": "stockimpacts"
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Prepare insert statement for News
sql = """
    INSERT INTO news (ticker, datePublished, headline, content, source, url)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

# Process each file
for json_file in json_files:
    print(f"\n📄 Processing {json_file.name}...")

    # Infer ticker from folder name or filename prefix
    ticker = json_file.parts[-2]  # subfolder name
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            content = json.load(file)
            articles = content.get("data", [])
    except Exception as e:
        print(f"❌ Failed to parse {json_file.name}: {e}")
        continue

    if not articles:
        print(f"⚠️ No data found in {json_file.name}")
        continue

    for article in articles:
        try:
            date = article.get("published_at")
            datePublished = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") if date else None
            headline = article.get("title")
            content = article.get("description") or article.get("snippet")
            source = article.get("source")
            url = article.get("url")

            cursor.execute(sql, (ticker, datePublished, headline, content, source, url))
        except Exception as err:
            print(f"❌ Skipping article due to error: {err}")

    conn.commit()
    print(f"✅ Inserted news from {json_file.name}")

# Close connection
cursor.close()
conn.close()
print("\n✅ All JSON files processed.")
