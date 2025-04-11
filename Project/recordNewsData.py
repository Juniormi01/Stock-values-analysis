from datetime import date, timedelta
import requests
import json


#In Y-m-d format
#From Janurary 13 - April 4th to align with the stock data

#6 tickers * 5 = 30 requests per week
#Do 2025-04-01 -> 2025-04-04 3 weeks, Should be 36 requests


start_date = date(2025, 3, 29)
end_date = date(2025, 3, 31)

current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:  # Monday to Friday are 0-4
        #Separate with commas, no spaces if adding multiple tickers
        tickers =  ['SPY', 'TSLA', 'LMT', 'META', 'BA', 'NVDA']
        for ticker in tickers:
            fileName = f"newsData\\{ticker}\\newsData"
            url = "https://api.marketaux.com/v1/news/all"
            parameters = {
                'symbols' : ticker,
                'filer_entities':'true',
                'language':'en',
                'api_token':'QmQ6R4LG9nKkln9FBM7rj7suS0rmAQ47eW0OW9hv',
                'limit': 1,
                'published_on':current_date                
            }
            #add the symbol name + the date published
            fileName += parameters["symbols"] + parameters["published_on"].strftime("%Y-%m-%d")

            response = requests.get(url, params=parameters)

            if response.status_code == 200:
                with open(fileName, "w") as file:
                    data = response.json()
                    json.dump(data, file, indent=4)
            else:
                print("ERROR, DATA NOT FETCHED")
            fileName = fileName[:len(fileName) - len(ticker) - len(parameters["published_on"].strftime("%Y-%m-%d"))]
    current_date += timedelta(days=1)
