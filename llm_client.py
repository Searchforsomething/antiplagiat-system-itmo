import json
import logging
import os

import requests
from dotenv import load_dotenv
from google import genai

from constants import OPENROUTER_MODELS, OPENROUTER_API_URL, GEMINI_MODELS, GENERATION_PROMPT_ADDITION

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("LLMClient")


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

            try:
                response = requests.post(OPENROUTER_API_URL, data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    try:
                        results[model_name] = response.json().get("choices")[0].get("message").get("content")
                        logger.info("%s output received successfully", model_name)

                    except Exception:
                        logger.error("Failed to parse response from model %s.", model_name)
                else:
                    logger.error("Failed to fetch data from model %s. Status Code: %s", model_name,
                                 response.status_code)

            except Exception:
                logger.error(f"Failed to get response from model %s.", model_name)

        return results

    def get_gemini_responses(self) -> dict:
        gemini_client = genai.Client()
        results = {}

        for model_name, model_id in GEMINI_MODELS.items():
            try:
                response = gemini_client.models.generate_content(
                    model=model_id, contents=self.role + self.task
                )
                results[model_name] = response.text
                logger.info("%s output received successfully", model_name)
            except Exception:
                logger.error("Failed to get response from model %s.", model_name)

        return results
