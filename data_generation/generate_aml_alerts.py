import pandas as pd

# -----------------------------------
# Load Data
# -----------------------------------

transactions_df = pd.read_csv(
    "generated_data/transactions.csv"
)

# -----------------------------------
# Alert Mapping
# -----------------------------------

ALERT_MAPPING = {

    "P1_CASH_STRUCTURING":
    (
        "Cash Structuring",
        "HIGH"
    ),

    "P2_LARGE_LATE_NIGHT":
    (
        "Large Late Night Activity",
        "MEDIUM"
    ),

    "P3_ACCOUNT_TAKEOVER":
    (
        "Account Takeover",
        "CRITICAL"
    ),

    "P4_ROUND_TRIPPING":
    (
        "Round Tripping",
        "HIGH"
    ),

    "P5_CROSS_BORDER_BURST":
    (
        "Cross Border Burst",
        "CRITICAL"
    ),

    "P6_DORMANT_REACTIVATION":
    (
        "Dormant Account Reactivation",
        "HIGH"
    ),

    "P7_CTR_THRESHOLD_SPLITTING":
    (
        "CTR Threshold Splitting",
        "HIGH"
    ),

    "P8_PEP_ACTIVITY":
    (
        "PEP Suspicious Activity",
        "CRITICAL"
    )

}

# -----------------------------------
# Generate AML Alerts
# -----------------------------------

aml_alerts = []

alert_counter = 1

fraud_transactions = transactions_df[

    transactions_df[
        "fraud_pattern"
    ] != "NORMAL"

]

for _, row in fraud_transactions.iterrows():

    alert_type, severity = ALERT_MAPPING.get(

        row["fraud_pattern"],

        (
            "Suspicious Activity",
            "MEDIUM"
        )

    )

    aml_alerts.append(

        {

            "alert_id":
            f"ALERT{alert_counter:09d}",

            "account_id":
            row["account_id"],

            "txn_id":
            row["txn_id"],

            "alert_type":
            alert_type,

            "severity":
            severity,

            "status":
            "OPEN",

            "created_at":
            row["txn_time"]

        }

    )

    alert_counter += 1

# -----------------------------------
# DataFrame
# -----------------------------------

aml_alerts_df = pd.DataFrame(
    aml_alerts
)

# -----------------------------------
# Validation
# -----------------------------------

assert aml_alerts_df[
    "alert_id"
].is_unique

assert aml_alerts_df[
    "account_id"
].notna().all()

assert aml_alerts_df[
    "alert_type"
].notna().all()

# -----------------------------------
# Save
# -----------------------------------

output_path = (
    "generated_data/"
    "aml_alerts.csv"
)

aml_alerts_df.to_csv(

    output_path,

    index=False

)

# -----------------------------------
# Summary
# -----------------------------------

print("=" * 60)
print(
    "AML Alerts Generation Completed"
)
print("=" * 60)

print(
    f"Total AML Alerts : "
    f"{len(aml_alerts_df)}"
)

print()

print(
    "Alert Type Distribution"
)

print(

    aml_alerts_df[
        "alert_type"
    ].value_counts()

)

print()


print(
    f"CSV Saved Successfully : "
    f"{output_path}"
)

print("=" * 60)