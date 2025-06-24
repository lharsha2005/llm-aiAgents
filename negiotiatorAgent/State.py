from typing import TypedDict

class State(TypedDict):
    img_path: str
    ocr_data: str
    extractor_data: str
    history: list[str]
    debate_flag: bool
    negotiator_flag: bool
    negotiator_data: str
    feedback: str
    round: int
    max_rounds: int