import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the API
genai.configure(api_key=GOOGLE_API_KEY)

class ChatGemini:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def get_gemini_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
