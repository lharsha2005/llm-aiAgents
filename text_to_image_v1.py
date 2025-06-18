import os
import torch
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from diffusers import StableDiffusionPipeline
from PIL import Image

load_dotenv()

pipe=StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_auth_token=os.getenv("HUGGINGFACE_API_KEY"))

prompt=PromptTemplate(
    input_variables=["img_dec"],
    template="Generate an image based on the following description:{img_dec}"
)

class ImageGenerator(Runnable):
    def invoke(self, input: str, x) -> str:
        if hasattr(input, "to_string"):
            input = input.to_string()
        image = pipe(input).images[0]
        image.save("generated_image.png")
        return "Image saved as 'generated_image.png'"

chain=prompt | ImageGenerator()

result = chain.invoke({"img_dec": "Sunrise over a calm horizon with silhouettes of birds flying in the sky, cinematic lighting”"})
print(result)
