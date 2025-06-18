import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
# from langchain_openai import openai
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")    

# llm=OpenAI(model="dall-e-3",api_key=os.getenv("OPENAI_API_KEY"))

prompt=PromptTemplate(
    input_variables=["img_desc"],
    template="generate an image with close resemblance to the following description:{img_desc}"
)

msg=prompt.format(img_desc="a boat in sea.")

res=openai.images.generate(
    model="dall-e-3",
    prompt=msg,
    n=1,
)

print(res.data[0].url)
