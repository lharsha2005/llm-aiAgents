from paddleocr import PaddleOCR
import cv2
import os

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)  # Use CPU for safety

def run_ocr(img_path: str):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image path does not exist: {img_path}")

    result = ocr.ocr(img_path)  # Don't read with cv2 unless needed

    lines = []
    if result and isinstance(result[0], list):
        for line in result[0]:
            lines.append(line[1][0])

    print("returning to supervisor")
    return "\n".join(lines)
