"""
LLM interface and OpenAI implementation.

The rest of the application should not need to know which
language model is being used.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from src.schemas import DeepDiveAnalysis, LLMEvaluation


load_dotenv()


class LLMClient:
    """
    Base interface for a reasoning engine.
    """

    def generate(self, prompt: str) -> dict:
        """
        Generate a structured response from a prompt.

        Concrete LLM implementations override this method.
        """

        raise NotImplementedError

    def generate_deep_dive(self, prompt: str) -> DeepDiveAnalysis:
        """
        Generate a detailed analysis for a selected job.

        Concrete LLM implementations override this method.
        """

        raise NotImplementedError


class OpenAIClient(LLMClient):
    """
    OpenAI implementation of the LLM interface.
    """

    def __init__(self, model: str):
        self.model = model

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set."
            )

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> LLMEvaluation:
        """
        Send a prompt to OpenAI and return a validated evaluation.
        """

        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=LLMEvaluation,
        )

        return response.output_parsed

    def generate_deep_dive(self, prompt: str) -> DeepDiveAnalysis:
        """
        Send a detailed analysis prompt to OpenAI and return
        a validated deep-dive analysis.
        """

        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=DeepDiveAnalysis,
        )

        return response.output_parsed