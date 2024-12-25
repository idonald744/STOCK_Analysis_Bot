from kafka import KafkaProducer
import json
import yfinance as yf
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def stream_stock_price():
    ticker = input("Enter stock ticker to stream: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    stock = yf.Ticker(ticker)
    
    while True:
        data = stock.history(start=start_date, end=end_date)
        if not data.empty:
            price = data['Close'].iloc[-1]
            payload = {"ticker": ticker, "price": price, "start_date": start_date, "end_date": end_date}
            producer.send('stock_prices', value=payload)
        else:
            print("No data available for the given period.")
        time.sleep(60)
