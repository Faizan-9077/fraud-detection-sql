# query_engine/services/prompt_builder.py

from prompt.system_prompt import SYSTEM_PROMPT
from prompt.aml_schema import AML_SCHEMA_CONTEXT
from prompt.few_shots import FEW_SHOT_EXAMPLES


class PromptBuilder:

    @staticmethod
    def build(question: str) -> str:
        return f"""
{SYSTEM_PROMPT}

==================================================
AML SCHEMA
==================================================

{AML_SCHEMA_CONTEXT}

==================================================
FEW SHOT EXAMPLES
==================================================

{FEW_SHOT_EXAMPLES}

==================================================
ANALYST QUESTION
==================================================

{question}

Return SQL only.
"""
    