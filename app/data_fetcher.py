import yfinance as yf
from polygon import RESTClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def get_stock_data(ticker: str):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data.to_dict()

def get_polygon_data(ticker: str):
    client = RESTClient(POLYGON_API_KEY)
    aggs = client.get_aggs(ticker, 1, "day", "2023-01-01", "2023-12-01")
    
    return [{"date": agg.timestamp, "close": agg.close} for agg in aggs]
