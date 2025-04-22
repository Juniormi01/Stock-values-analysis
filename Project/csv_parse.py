import csv
import os
from pathlib import Path

# Directory containing downloaded stock CSVs
csv_dir = Path('./data/')
# Output SQL file
dest_file = Path('./sql_files/insert_daily_metrics.sql')
dest_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

# Function to extract stock symbol from filename
def get_stock_symbol(filename):
    return filename.name.split('_')[0]

# Function to generate SQL insert commands from CSV
def generate_sql_insertions(csv_file):
    stock_symbol = get_stock_symbol(csv_file)
    sql_commands = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        next(reader)  # Skip header
        for row in reader:
            date, open_price, high, low, close, volume = row[0], row[1], row[2], row[3], row[4], row[5]
            sql = (
                "INSERT INTO Stocks (ticker, date, openPrice, closePrice, highPrice, lowPrice, volume) "
                f"VALUES ('{stock_symbol}', '{date}', {open_price}, {close}, {high}, {low}, {volume});"
            )
            sql_commands.append(sql)

    return sql_commands

# Get all CSV files from directory
csv_files = sorted(csv_dir.glob("*_data.csv"))

# Write SQL insertions to file
with open(dest_file, 'w') as sql_file:
    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        sql_insertions = generate_sql_insertions(csv_file)
        sql_file.write(f"-- {csv_file.name}\n")
        sql_file.write('\n'.join(sql_insertions) + '\n')
    print(f"SQL insertion commands saved to {dest_file}")

print("All CSV files processed.")
