from typing import TypedDict

class State(TypedDict):
    stock: str
    news: str
    sentiment: str
    round: int
    max_rounds: int
    history: str
    stock_data: dict
    recommendation: str