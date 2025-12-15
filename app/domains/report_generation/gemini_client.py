import asyncio

from google import generativeai as genai


class GeminiClient:
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key

        self.configure_gemini()

    def configure_gemini(self) -> None:
        genai.configure(api_key=self.api_key)

    async def generate(self, prompt: str) -> str:
        model = genai.GenerativeModel(model_name=self.model_name)

        def _generate_content() -> str:
            response = model.generate_content(prompt)
            return (response.text or "").strip()

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _generate_content)
