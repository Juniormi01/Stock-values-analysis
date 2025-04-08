import json
import mysql.connector
from pathlib import Path

# Directory containing JSON files
json_dir = Path('./json_data/')

# MySQL connection settings
db_config = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Get all JSON files in the directory
json_files = sorted(json_dir.glob("*.json"))

# Process each JSON file
for json_file in json_files:
    print(f"Processing {json_file.name}...")

    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse {json_file.name}: {e}")
            continue

    if data:
        for row in data:
            columns = ", ".join(row.keys())
            placeholders = ", ".join(["%s"] * len(row))
            values = tuple(row.values())

            sql = f"INSERT INTO  Stocks({columns}) VALUES ({placeholders})"
            try:
                cursor.execute(sql, values)
            except mysql.connector.Error as err:
                print(f"❌ Error inserting row in {json_file.name}: {err}")
        conn.commit()
        print(f"✅ Inserted data from {json_file.name}")
    else:
        print(f"⚠️ No data found in {json_file.name}")

# Close MySQL connection
cursor.close()
conn.close()
print("All JSON files processed.")
