from openai import OpenAI
import base64
import mimetypes
from langgraph.types import Command
from State import State
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def vision(state: State) -> Command:
    img_path = state["img_path"]
    if not img_path or not os.path.exists(img_path):
        raise FileNotFoundError(f"Image path not found: {img_path}")

    mime_type, _ = mimetypes.guess_type(img_path)
    if mime_type is None:
        mime_type = "image/png"

    base64_img = encode_image_to_base64(img_path)
    image_data_url = f"data:{mime_type};base64,{base64_img}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ],
        max_tokens=1024
    )

    return Command(
        update={"ocr_text": response.choices[0].message.content, "img_path": None},
        goto="supervisor"
    )
