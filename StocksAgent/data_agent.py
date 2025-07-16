import yfinance as yf
from langgraph.types import Command

from State import State

def run_stock_data(state: State):
    stock = state["stock"]

    try:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="5d", interval="1d")

        # Just extract simple values
        latest_close = hist["Close"].iloc[-1]
        previous_close = hist["Close"].iloc[-2]
        price_change = latest_close - previous_close
        percent_change = (price_change / previous_close) * 100

        summary = {
            "latest_close": round(latest_close, 2),
            "previous_close": round(previous_close, 2),
            "price_change": round(price_change, 2),
            "percent_change": round(percent_change, 2)
        }

        return Command(update={"stock_data": summary},goto="predictor")

    except Exception as e:
        return Command(update={"stock_data": None},goto="predictor")
    