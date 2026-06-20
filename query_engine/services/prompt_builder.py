# query_engine/services/prompt_builder.py

from prompts.system_prompt import SYSTEM_PROMPT
from prompts.few_shots import FEW_SHOTS
from prompts.aml_schema import AML_SCHEMAS


class PromptBuilder:

    KEYWORD_MAPPING = {
        # Cross Border
        "fatf": ["cross_border"],
        "cross border": ["cross_border"],
        "international": ["cross_border"],
        "foreign": ["cross_border"],

        # Structuring
        "structuring": ["structuring"],
        "smurfing": ["structuring"],
        "ctr": ["structuring"],
        "cash deposits": ["structuring"],

        # Dormant
        "dormant": ["dormant"],
        "inactive account": ["dormant"],

        # Alerts
        "alert": ["alerts"],
        "alerts": ["alerts"],
        "investigation": ["alerts"],
        "investigate": ["alerts"],
        "suspicious": ["alerts"],
        "suspicious activity": ["alerts"],
        "fraud": ["alerts"],
        "aml": ["alerts"],

        # Risk
        "risk": ["risk"],
        "high risk": ["risk"],
        "flagged": ["risk"],
        "flagged customer": ["risk"],
        "flagged customers": ["risk"],
        "risky customer": ["risk"],
        "risky customers": ["risk"],
        "compliance": ["risk"],

        # Velocity
        "velocity": ["velocity"],
        "rapid": ["velocity"],
        "burst": ["velocity"],

        # Takeover
        "takeover": ["takeover"],
        "device mismatch": ["takeover"],

        # KYC
        "kyc": ["kyc"],
        "expired kyc": ["kyc"],
        "overdue kyc": ["kyc"],

        # Round Trip
        "round trip": ["round_trip"],
        "round-tripping": ["round_trip"],
        "circular": ["round_trip"],

        # Travel
        "travel": ["travel"],
        "impossible travel": ["travel"],

        # Mule
        "mule": ["mule"],

        # Beneficiary
        "beneficiary": ["beneficiary"],

        # SLA
        "sla": ["sla"],
        "aging": ["sla"],

        # Night Transactions
        "night": ["alerts"],
        "night transaction": ["alerts"],
        "night transactions": ["alerts"],
        "late night": ["alerts"],
        "midnight": ["alerts"],

        # Additional Views
        "device": ["device"],
        "login": ["device"],
        "sar": ["sar"],
        "branch": ["branch"],
        "new account": ["new_account"],
        "transaction": ["transaction"],

        # Transaction Core
        "transactions": ["transaction"],
        "failed transactions": ["transaction"],
        "failed transaction": ["transaction"],
        "amount": ["transaction"],

        # Time Based Queries
        "11 pm": ["transaction"],
        "4 am": ["transaction"],
        "overnight": ["transaction"],
        "after midnight": ["transaction"],

        # Cross Border
        "cross-border": ["cross_border"],
        "high-risk country": ["cross_border"],
        "high-risk countries": ["cross_border"],
        "fatf country": ["cross_border"],
        "fatf countries": ["cross_border"],

        # Structuring
        "structuring activity": ["structuring"],
        "cash structuring": ["structuring"],

        # Velocity
        "one hour": ["velocity"],
        "1 hour": ["velocity"],
        "20 transactions": ["velocity"],
        "rapid transactions": ["velocity"],

        # Beneficiary
        "beneficiaries": ["beneficiary"],
        "shared beneficiaries": ["beneficiary"],
    }

    @classmethod
    def _select_examples(cls, question: str) -> str:

        question_lower = question.lower()

        selected = []

        for keyword, examples in cls.KEYWORD_MAPPING.items():

            if keyword in question_lower:

                for example in examples:

                    if example in FEW_SHOTS and example not in selected:
                        selected.append(example)

        # fallback examples
        if not selected:
            selected = [
                "risk",
                "alerts",
                "cross_border"
            ]

        selected = selected[:5]

        return "\n\n".join(
            FEW_SHOTS[name]
            for name in selected
        )

    @classmethod
    def _select_schema(cls, question: str) -> str:

        question_lower = question.lower()

        selected = []

        for keyword, schemas in cls.KEYWORD_MAPPING.items():

            if keyword in question_lower:

                for schema in schemas:

                    if schema in AML_SCHEMAS and schema not in selected:
                        selected.append(schema)

        # stronger fallback
        if not selected:
            selected = [
                "alerts",
                "risk",
                "cross_border",
                "transaction",
                "velocity"
            ]

        selected = selected[:5]

        return "\n\n".join(
            AML_SCHEMAS[name]
            for name in selected
        )

    @classmethod
    def build(cls, question: str) -> str:

        few_shots = cls._select_examples(question)
        schema_context = cls._select_schema(question)

        return f"""
{SYSTEM_PROMPT}

==================================================
AML SCHEMA
==================================================

{schema_context}

==================================================
FEW SHOT EXAMPLES
==================================================

{few_shots}

==================================================
ANALYST QUESTION
==================================================

{question}

Return SQL only.
"""