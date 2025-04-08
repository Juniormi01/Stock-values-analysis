import csv
import os

def createInserts(file):
    ticker = file.split()   #needs changing
    sql  = []
    with open(file, 'f') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            sql = f"INSERT INTO Stocks (ticker, company, date, openPrice, closePrice, highPrice, lowPrice, volume)"
            
