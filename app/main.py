from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from app.data_fetcher import get_stock_data, get_polygon_data
from app.gpt_analyzer import analyze_with_gpt
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from polygon import RESTClient
import asyncio
import threading
from dashboards.stock_dashboard import run_dash

# Load environment variables
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
client = RESTClient(POLYGON_API_KEY)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stock Analysis API is running"}

@app.get("/stock/{ticker}")
def fetch_stock(ticker: str):
    data = get_stock_data(ticker)  # Pass ticker directly as an argument
    if not data:
        raise HTTPException(status_code=404, detail="Stock not found")
    return data

class StockData(BaseModel):
    data: dict

@app.post("/analyze/")
def analyze_stock(stock_data: StockData):
    result = analyze_with_gpt(stock_data.data)
    return {"recommendation": result}

@app.websocket("/ws/stock/{ticker}")
async def websocket_endpoint(websocket: WebSocket, ticker: str):
    await websocket.accept()
    try:
        while True:
            aggs = client.get_aggs(ticker, 1, "minute", "2023-01-01", "2023-12-01")
            if aggs:
                latest = aggs[-1]
                price = latest.close
                await websocket.send_json({"ticker": ticker, "price": price})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print(f"Client disconnected from {ticker} stream")

# Start Dash app in a separate thread
threading.Thread(target=run_dash).start()
