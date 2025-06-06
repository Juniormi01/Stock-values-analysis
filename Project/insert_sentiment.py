import json
import psycopg2
from pathlib import Path
from datetime import datetime
from textblob import TextBlob

# Directory containing subfolders like BA, META, etc.
json_dir = Path('./newsData/')

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

# Helper: classify sentiment label from polarity score
def classify_sentiment(score):
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Step 1: Fetch all news articles with their IDs
cursor.execute("SELECT id, content, ticker FROM news")
news_items = cursor.fetchall()

inserted = 0
for news_id, content, ticker in news_items:
    if content:
        blob = TextBlob(content)
        score = round(blob.sentiment.polarity, 3)
        label = classify_sentiment(score)

        try:
            cursor.execute("""
                INSERT INTO Sentiment (NewsID, ticker, score, label)
                VALUES (%s, %s, %s, %s)
            """, (news_id, ticker, score, label))
            inserted += 1
        except Exception as e:
            print(f"❌ Failed to insert sentiment for NewsID {news_id}: {e}")

conn.commit()
print(f"✅ Inserted sentiment for {inserted} articles")

cursor.close()
conn.close()
