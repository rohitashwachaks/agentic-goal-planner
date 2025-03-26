# llm/llm_wrapper.py

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


class LLMRouter:
    def __init__(self):
        self.llm_type = os.getenv("USE_LLM", "gpt4o").lower()
        self.model = os.getenv("LITELLM_MODEL_NAME", "gpt-4o")

        # For Ollama (custom route override)
        if self.llm_type == "ollama":
            self.model = os.getenv('LITELLM_OLLAMA_MODEL', 'ollama/mistral')

    def get_llm(self):
        return completion(model=self.model)  # ✅ This is what CrewAI expects

    def get_model_name(self):
        return self.model
