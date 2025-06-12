import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def llm_model(prompt, parameter, model):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model)

    # Send the image + prompt
    result = model.generate_content([
        prompt,parameter
    ])

    return result.text