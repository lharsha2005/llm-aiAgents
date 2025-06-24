from paddleocr import PaddleOCR
from State import State
from langgraph.types import Command
import cv2
import os

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False) # Use CPU for safety

def run_ocr(state: State)->State:
    img_path=state["img_path"]
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image path does not exist: {img_path}")

    result = ocr.ocr(img_path)  # Don't read with cv2 unless needed

    lines = []
    if result and isinstance(result[0], list):
        for line in result[0]:
            lines.append(line[1][0])

    print("ocr->supervisor")
    result="\n".join(lines)
    return Command(update={"ocr_data":result},goto="supervisor")