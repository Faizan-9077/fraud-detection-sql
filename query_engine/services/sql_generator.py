# query_engine/services/sql_generator.py

import logging

from llm.config import LLM_PROVIDER

from llm.llama_client import LlamaClient
from llm.groq_client import GroqClient

from query_engine.services.prompt_builder import PromptBuilder


logger = logging.getLogger(__name__)


class SQLGenerator:

    def __init__(self):

        if LLM_PROVIDER.lower() == "groq":
            self.client = GroqClient()
        else:
            self.client = LlamaClient()

    def generate_sql(self, question: str) -> str:

        prompt = PromptBuilder.build(question)

        logger.info("Generating SQL")
        logger.info(f"Question: {question}")

        response = self.client.generate(prompt)

        if not response:
            raise ValueError(
                "LLM returned empty response."
            )

        sql = response.strip()

        logger.info(f"Generated SQL:\n{sql}")

        return sql