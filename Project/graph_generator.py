import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="localhost",       # change if remote
    database="StockImpacts",
    user="your_username",
    password="your_password"
)

# SQL query to fetch stock price data
query = """
SELECT date, close_price
FROM stock_prices
WHERE symbol = 'LMT'
ORDER BY date;
"""

# Load into a DataFrame
df = pd.read_sql_query(query, conn)
df['date'] = pd.to_datetime(df['date'])

# Optional: Calculate a 10-day rolling average
df['rolling_avg'] = df['close_price'].rolling(window=10).mean()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close_price'], label='Close Price', linewidth=2)
plt.plot(df['date'], df['rolling_avg'], label='10-Day Rolling Avg', linestyle='--')

# Highlight variance
plt.fill_between(df['date'], df['rolling_avg'], df['close_price'],
                 where=(df['close_price'] > df['rolling_avg']),
                 color='green', alpha=0.3, interpolate=True, label='Above Avg')

plt.fill_between(df['date'], df['rolling_avg'], df['close_price'],
                 where=(df['close_price'] < df['rolling_avg']),
                 color='red', alpha=0.3, interpolate=True, label='Below Avg')

plt.title('LMT Stock Price & Variance')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Close the connection
conn.close()
