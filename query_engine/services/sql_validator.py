# query_engine/services/sql_validator.py

import re


class SQLValidationError(Exception):
    pass


class SQLValidator:

    ALLOWED_VIEWS = {
        "vw_transaction_core",
        "vw_cross_border_risk",
        "vw_structuring_detection",
        "vw_dormant_account_activity",
        "vw_aml_alert_investigation",
        "vw_customer_risk_profile",
        "vw_device_login_anomaly",
        "vw_sar_evidence_packet",
        "vw_velocity_rapid_fire",
        "vw_account_takeover_signal",
        "vw_kyc_lapsed_high_risk",
        "vw_round_trip_detection",
        "vw_impossible_travel",
        "vw_branch_concentration_risk",
        "vw_mule_account_pattern",
        "vw_new_account_fraud",
        "vw_shared_beneficiary_network",
        "vw_alert_aging_sla",
    }

    FORBIDDEN_KEYWORDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    }

    FORBIDDEN_SYSTEM_OBJECTS = {
        "PG_",
        "INFORMATION_SCHEMA",
    }

    @staticmethod
    def clean_sql(sql: str) -> str:
        sql = sql.strip()

        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")

        return sql.strip()

    @classmethod
    def validate(cls, sql: str) -> str:

        sql = cls.clean_sql(sql)

        sql_upper = sql.upper()

        # --------------------------------------------------
        # Rule 1: Only SELECT / WITH
        # --------------------------------------------------

        if not (
            sql_upper.startswith("SELECT")
            or sql_upper.startswith("WITH")
        ):
            raise SQLValidationError(
                "Only SELECT and WITH queries are allowed."
            )

        # --------------------------------------------------
        # Rule 2: Block multiple statements
        # --------------------------------------------------

        sql_no_space = sql.strip()

        if ";" in sql_no_space[:-1]:
            raise SQLValidationError(
                "Multiple SQL statements are not allowed."
            )

        # --------------------------------------------------
        # Rule 3: Block dangerous keywords
        # --------------------------------------------------

        for keyword in cls.FORBIDDEN_KEYWORDS:

            if re.search(
                rf"\b{keyword}\b",
                sql_upper,
            ):
                raise SQLValidationError(
                    f"Forbidden SQL keyword detected: {keyword}"
                )

        # --------------------------------------------------
        # Rule 4: Block system catalog access
        # --------------------------------------------------

        for system_object in cls.FORBIDDEN_SYSTEM_OBJECTS:

            if system_object in sql_upper:
                raise SQLValidationError(
                    f"Forbidden system object: {system_object}"
                )

        # --------------------------------------------------
        # Rule 5: Validate FROM/JOIN targets
        # --------------------------------------------------

        tables_used = re.findall(
            r"(?:FROM|JOIN)\s+([a-zA-Z0-9_]+)",
            sql,
            flags=re.IGNORECASE,
        )

        if not tables_used:
            raise SQLValidationError(
                "No AML view found in query."
            )

        allowed_views_lower = {
            view.lower()
            for view in cls.ALLOWED_VIEWS
        }

        for table in tables_used:

            if table.lower() not in allowed_views_lower:

                raise SQLValidationError(
                    f"Unauthorized table/view detected: {table}"
                )

        # --------------------------------------------------
        # Rule 6: Auto LIMIT protection
        # --------------------------------------------------

        if not re.search(
            r"\bLIMIT\s+\d+\b",
            sql_upper
        ):

            sql = sql.rstrip(";")

            sql += "\nLIMIT 100;"

        return sql