import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_with_gpt(stock_data):
    prompt = f"Analyze this stock data: {stock_data}. Suggest buy/sell points."
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()