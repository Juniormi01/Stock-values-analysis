create DATABASE  StockImpacts

create TABLE Stocks(
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    company VARCHAR(100),
    date DATE,
    openPrice DECIMAL(10,2),
    closePrice DECIMAL(10,2),
    highPrice DECIMAL(10,2),
    lowPrice DECIMAL(10,2),
    volume INT

)

create TABLE News(
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    datePublished TIMESTAMP NOT NULL,
    headline TEXT NOT NULL,
    content TEXT,
    source VARCHAR(255),
    url TEXT
)

CREATE TABLE StockMetaData(
    ticker VARCHAR(10) PRIMARY KEY,
    comany VARCHAR(255),
    industry VARCHAR(255),
    sector VARCHAR(255),
    marketCap Decimal(15,2),
    hq VARCHAR(255)
)

CREATE TABLE Sentiment(
    id SERIAL PRIMARY KEY,
    NewsID INT NOT NULL,
    ticker VARCHAR(10),
    score DECIMAL(5,2) CHECK (score BETWEEN -1 AND 1),
    label VARCHAR(10) CHECK (label IN ('Positive', 'Neutral', 'Negative')),

)