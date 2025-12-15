from typing import Protocol


class ILLMClient(Protocol):
    async def generate(self, prompt: str) -> str: ...
