import json
import os

import requests
from dotenv import load_dotenv
from google import genai

from constants import OPENROUTER_MODELS, OPENROUTER_API_URL, GEMINI_MODELS, GENERATION_PROMPT_ADDITION



class LLMClient:
    def __init__(self, task: str):
        self.task = task + GENERATION_PROMPT_ADDITION
        self.role = "Ты - эксперт в программировании."

        load_dotenv()

    def get_openrouter_responses(self) -> dict:
        results = {}

        headers = {
            'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
            'Content-Type': 'application/json'
        }
        for model_name, model_id in OPENROUTER_MODELS.items():

            data = {
                "model": model_id,
                "messages": [{"role": "system", "content": self.role},
                             {"role": "user", "content": self.task}]
            }

            response = requests.post(OPENROUTER_API_URL, data=json.dumps(data), headers=headers)

            if response.status_code == 200:
                try:
                    results[model_name] = response.json().get("choices")[0].get("message").get("content")
                except Exception:
                    results[model_name] = None
            else:
                print(f"Failed to fetch data from model {model_name}. Status Code:", response.status_code)

        return results

    def get_gemini_response(self) -> dict:
        gemini_client = genai.Client()
        results = {}

        for model_name, model_id in GEMINI_MODELS.items():
            response = gemini_client.models.generate_content(
                model=model_id, contents=self.role + self.task
            )
            print(response.text)

            results[model_name] = response.text

        return results

