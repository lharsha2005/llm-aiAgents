from typing import TypedDict,Optional

class State(TypedDict):
    img_path: Optional[str]
    question: str
    ocr_text: str
    answer: str