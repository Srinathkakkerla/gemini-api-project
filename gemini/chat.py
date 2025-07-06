import google.generativeai as genai
from dotenv import load_dotenv
import os

class ChatGemini:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        # Initialize the Gemini model
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    def get_gemini_response(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
