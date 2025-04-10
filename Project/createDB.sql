-- Create Stocks table
CREATE TABLE Stocks (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    date DATE,
    openPrice DECIMAL(10,2),
    closePrice DECIMAL(10,2),
    highPrice DECIMAL(10,2),
    lowPrice DECIMAL(10,2),
    volume INT
);

-- Create News table
CREATE TABLE News (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    datePublished TIMESTAMP NOT NULL,
    headline TEXT NOT NULL,
    content TEXT,
    source VARCHAR(255),
    url TEXT
);

-- Create StockMetaData table
CREATE TABLE StockMetaData (
    ticker VARCHAR(10) PRIMARY KEY,
    company VARCHAR(255),
    industry VARCHAR(255),
    sector VARCHAR(255),
    marketCap DECIMAL(15,2),
    hq VARCHAR(255)
);

-- Create Sentiment table
CREATE TABLE Sentiment (
    id SERIAL PRIMARY KEY,
    NewsID INT NOT NULL,
    ticker VARCHAR(10),
    score DECIMAL(5,2) CHECK (score BETWEEN -1 AND 1),
    label VARCHAR(10) CHECK (label IN ('Positive', 'Neutral', 'Negative'))
);

-- Add foreign key constraints
ALTER TABLE Stocks
ADD FOREIGN KEY (ticker) REFERENCES StockMetaData(ticker);

ALTER TABLE News
ADD FOREIGN KEY (ticker) REFERENCES StockMetaData(ticker);

ALTER TABLE Sentiment
ADD FOREIGN KEY (ticker) REFERENCES StockMetaData(ticker),
ADD FOREIGN KEY (NewsID) REFERENCES News(id);