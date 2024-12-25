import dash
from dash import dcc, html
import dash.dependencies as dd
import threading
import json
import asyncio
import websockets

# Initialize Dash app
dash_app = dash.Dash(__name__, url_base_pathname='/dashboard/')

# Dash Layout
dash_app.layout = html.Div([
    html.H1("Real-time Stock Prices"),
    dcc.Input(id='ticker-input', type='text', value='AAPL', debounce=True),
    html.Div(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=5000,  # 5 seconds
        n_intervals=0
    )
])

# WebSocket Client for Dash
@dash_app.callback(
    dd.Output('live-update-text', 'children'),
    [dd.Input('interval-component', 'n_intervals'),
     dd.Input('ticker-input', 'value')]
)
def update_price(n, ticker):
    uri = f'ws://127.0.0.1:8000/ws/stock/{ticker}'
    async def fetch_price():
        async with websockets.connect(uri) as websocket:
            response = await websocket.recv()
            data = json.loads(response)
            return f"{ticker} Price: ${data['price']:.2f}"
    
    return asyncio.run(fetch_price())

# Run Dash server
def run_dash():
    dash_app.run_server(debug=True, use_reloader=False)
