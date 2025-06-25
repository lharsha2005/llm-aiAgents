from paddleocr import PaddleOCR
from State import State
from langgraph.types import Command
import cv2
import os

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
def run_ocr(state: State)->State:
    img_path=state["img_path"]
    if img_path==None:
        return Command(update={"img_path": None},goto="supervisor")
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image path does not exist: {img_path}")

    result = ocr.ocr(img_path)

    lines = []
    if result and isinstance(result[0], list):
        for line in result[0]:
            lines.append(line[1][0])

    print("ocr->supervisor")
    result="\n".join(lines)
    return Command(update={"ocr_text":result,"img_path": None},goto="supervisor")